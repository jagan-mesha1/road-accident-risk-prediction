# Road Accident Risk Prediction Using Machine Learning

A Flask-based web application that estimates road accident risk from road, traffic, weather, environmental and time-related inputs using a trained XGBoost model.

## Overview

This project demonstrates an end-to-end machine learning web application. Users can register or log in, enter road and environmental conditions through a web interface, and request an accident-risk prediction.

The application combines a Python/Flask backend, a browser-based frontend, trained model artifacts, and a MySQL database for user-related functionality.

## Features

- User registration and login
- Web form for submitting road and environmental conditions
- Machine-learning-based road accident risk prediction
- Data preprocessing and feature transformation before prediction
- Integration of a trained XGBoost model
- MySQL-backed user functionality

## Technology Stack

| Area | Technologies |
|---|---|
| Language | Python |
| Backend | Flask |
| Frontend | HTML, CSS, JavaScript |
| Machine Learning | XGBoost, scikit-learn |
| Data Processing | Pandas, NumPy |
| Database | MySQL |
| Model Serialization | Joblib, Pickle |

## Repository Structure

```text
road-accident-risk-prediction/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── database
├── models/
│   ├── feature_names.pkl
│   ├── random_forest_model.pkl
│   ├── scaler (1).pkl
│   └── xgboost_model.pkl
├── static/
│   ├── script.js
│   └── style.css
└── templates/
    ├── about.html
    ├── base.html
    ├── home.html
    ├── login.html
    ├── prediction.html
    └── register.html
```

## Getting Started

### Prerequisites

- Python installed on your machine
- MySQL Server
- Git

### 1. Clone the repository

```bash
git clone https://github.com/jagan-mesha1/road-accident-risk-prediction.git
cd road-accident-risk-prediction
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to a new file named `.env`, then edit `.env` with your local configuration. Set a private Flask secret key and the correct MySQL host, username, port, password and database name.

Do not commit `.env` or share database passwords and secret keys. The `.env.example` file is intended to contain placeholders only.

### 5. Set up MySQL

Start MySQL Server and create/configure the database and tables using the SQL script or instructions in the `database` item. Make sure the database settings in `.env` match your local MySQL configuration.

### 6. Run the application

```bash
python app.py
```

Open the local address shown by Flask in your browser. The default development address is usually:

```text
http://127.0.0.1:5000
```

## Security Notes

- Keep database credentials and the Flask secret key in your local `.env` file.
- `.env` is excluded from version control; `.env.example` documents the required variable names.
- User passwords are handled using bcrypt in the application.
- This project uses Flask's development server for local development. Do not use it as a production deployment server without appropriate production configuration.

## Project Purpose

The project explores how machine learning can be integrated into a web application to support data-driven road-safety analysis. Its predictions are estimates based on the model and supplied inputs; they should not be treated as definitive assessments of real-world road safety.

## Author

**Mesha Jagan**  
GitHub: [jagan-mesha1](https://github.com/jagan-mesha1)
