# Road Accident Risk Prediction Using Machine Learning

A machine learning-based web application that estimates road accident risk using road, traffic, environmental and time-related conditions.

## Project Overview

This project uses machine learning to analyse road-related factors and estimate accident risk. It provides a web interface where users can enter relevant conditions and receive a risk prediction.

## Features

- User registration and login
- Road accident risk prediction
- Analysis of road and weather conditions
- Feature engineering and data preprocessing
- Machine learning model integration
- Web-based user interface

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend | Flask |
| Frontend | HTML, CSS, JavaScript |
| Machine Learning | XGBoost |
| Data Processing | Pandas, NumPy |
| Database | MySQL |
| Model Storage | Joblib, Pickle |

## Project Structure

```text
road-accident-risk-prediction/
│
├── app.py
├── requirements.txt
├── .gitignore
├── .env.example
├── models/
├── templates/
├── static/
└── database/
```

## Installation and Setup

1. Clone this repository.
2. Create a Python virtual environment.
3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Configure your environment variables using `.env.example`.
5. Set up the MySQL database.
6. Start the application:

```bash
python app.py
```

7. Open `http://127.0.0.1:5000` in your browser.

## Security

- Database credentials are stored in environment variables.
- Private `.env` files are excluded from version control.
- Passwords are handled using bcrypt.

## Project Purpose

The objective is to demonstrate how machine learning can be integrated with a web application to support data-driven road safety analysis.

## Author

Mesha Jagan

GitHub: https://github.com/jagan-mesha1