from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import bcrypt
import pandas as pd
import joblib
import pickle
import webbrowser
import os
import subprocess
from threading import Timer
from dotenv import load_dotenv

load_dotenv(override=True)
app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

# ---------- Database connection ----------
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        port=int(os.getenv("DB_PORT", 3306)),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# ---------- Load ML artifacts ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, 'models')

model = joblib.load(os.path.join(MODEL_DIR, 'xgboost_model.pkl'))
scaler = joblib.load(os.path.join(MODEL_DIR, 'scaler (1).pkl'))

with open(os.path.join(MODEL_DIR, 'feature_names.pkl'), 'rb') as f:
    feature_names = pickle.load(f)

# ---------- Helper: preprocess prediction input ----------
def preprocess_input(data_dict):
    """Convert raw form data into model-ready DataFrame."""
    df = pd.DataFrame([data_dict])

    # Feature engineering (same as notebook)
    df['speed_curvature'] = df['speed_limit'] * df['curvature']
    df['reported_per_lane'] = df['num_reported_accidents'] / (df['num_lanes'] + 1)

    # One-hot encode categorical columns
    cat_cols = ['road_type', 'lighting', 'weather', 'road_signs_present',
                'public_road', 'time_of_day', 'holiday', 'school_season']
    df_encoded = pd.get_dummies(df, columns=cat_cols, drop_first=True)

    # Reindex to match training features (missing columns -> 0)
    df_encoded = df_encoded.reindex(columns=feature_names, fill_value=0)

    # Scale numerical features (only the original four)
    num_cols = ['num_lanes', 'curvature', 'speed_limit', 'num_reported_accidents']
    df_encoded[num_cols] = scaler.transform(df_encoded[num_cols])

    return df_encoded

# ---------- Helper: risk level + tailored suggestions ----------
def get_risk_level_and_suggestions(risk_score, input_data):
    """Return risk category, color, and a list of safety suggestions.
       Adjusted thresholds for this model (max observed ~0.57)."""
    # Adjusted thresholds: Low <0.45, Medium 0.45-0.53, High >=0.53
    if risk_score < 0.25:
        level = "Low"
        color = "green"
        base = [
            "✅ Low risk conditions. Continue following standard safety practices.",
            "📱 Stay attentive – even low-risk roads can have surprises.",
            "🔄 Regularly check mirrors and blind spots."
        ]
    elif risk_score < 0.50:
        level = "Medium"
        color = "orange"
        base = [
            "⚠️ Moderate accident risk. Stay alert and drive defensively.",
            "👀 Increase following distance to at least 3 seconds.",
            "📉 Reduce speed slightly, especially on curves or in traffic.",
            "🔧 Ensure your vehicle's brakes and tires are in good condition."
        ]
    else:   #risk_score >= 0.53
        level = "High"
        color = "red"
        base = [
            "🚨 HIGH RISK – Extra caution required!",
            "🐢 Reduce speed significantly below the posted limit.",
            "🚗 Avoid sudden lane changes or aggressive maneuvers.",
            "📞 Consider postponing non-essential travel.",
            "🆘 Keep emergency contact numbers handy."
        ]

    # Feature-specific suggestions
    specific = []

    # Road geometry
    if input_data['curvature'] > 0.6:
        specific.append("🔁 Sharp curve ahead – reduce speed and avoid sudden steering.")
    if input_data['speed_limit'] > 90:
        specific.append("🏁 High speed limit – increase following distance.")
    if input_data['num_reported_accidents'] > 20:
        specific.append("📉 Accident‑prone zone – drive slowly and watch for sudden braking.")

    # Weather
    if input_data['weather'] == 'Rainy':
        specific.append("🌧️ Wet road – increase gap, avoid hard braking.")
    if input_data['weather'] == 'Foggy':
        specific.append("🌫️ Low visibility – use fog lights and reduce speed.")

    # Lighting
    if input_data['lighting'] in ['Dim', 'Night']:
        specific.append("💡 Poor lighting – use high beams (when safe) and watch for pedestrians.")

    # Road type
    if input_data['road_type'] == 'Rural':
        specific.append("🌾 Unlit rural road – watch for animals and unexpected turns.")

    # Temporal factors
    if input_data['holiday']:
        specific.append("🎉 Holiday period – more erratic drivers, stay patient.")
    if input_data['school_season'] and input_data['time_of_day'] in ['Morning', 'Evening']:
        specific.append("🚸 School season – children crossing, obey speed limits near schools.")

    # Combine and limit to 4 suggestions for readability
    all_suggestions = (base + specific)[:4]
    return level, color, all_suggestions

# ---------- Routes ----------
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm_password']

        if password != confirm:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                (username, email, hashed)
            )
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            flash('Username or email already exists.', 'danger')
        finally:
            cursor.close()
            conn.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('prediction'))
        else:
            flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if 'user_id' not in session:
        flash('Please login to access the prediction page.', 'warning')
        return redirect(url_for('login'))

    risk_score = None
    risk_level = None
    suggestions = []
    color = ""

    if request.method == 'POST':
        # Collect form data
        input_data = {
            'num_lanes': int(request.form['num_lanes']),
            'curvature': float(request.form['curvature']),
            'speed_limit': int(request.form['speed_limit']),
            'num_reported_accidents': int(request.form['num_reported_accidents']),
            'road_type': request.form['road_type'],
            'lighting': request.form['lighting'],
            'weather': request.form['weather'],
            'road_signs_present': request.form['road_signs_present'],
            'public_road': request.form['public_road'] == 'True',
            'time_of_day': request.form['time_of_day'],
            'holiday': request.form['holiday'] == 'True',
            'school_season': request.form['school_season'] == 'True'
        }

        # Preprocess and predict
        X = preprocess_input(input_data)
        risk_score = model.predict(X)[0]

        # Get risk level and suggestions
        risk_level, color, suggestions = get_risk_level_and_suggestions(risk_score, input_data)

    return render_template('prediction.html',
                           risk_score=risk_score,
                           risk_level=risk_level,
                           suggestions=suggestions,
                           color=color)

if __name__ == '__main__':

    def open_chrome():
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(
                r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
            )
        ]

        for path in chrome_paths:
            if os.path.exists(path):
                subprocess.Popen([path, "http://127.0.0.1:5000"])
                return

        print("Google Chrome was not found.")

    Timer(2, open_chrome).start()

    app.run(debug=True, use_reloader=False)