from flask import Flask, request, jsonify
import sqlite3
import joblib
import datetime
import numpy as np
import pandas as pd

app = Flask(__name__)
DATABASE = 'aqi_data.db'
MODEL_PATH = 'C:\\Users\\ASUS\\OneDrive\\Desktop\\AQI\\random_forest_model.pkl'

# Initialize the database
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS aqi_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            PM25 REAL,
            PM10 REAL,
            SO2 REAL,
            NOx REAL,
            NH3 REAL,
            CO REAL,
            O3 REAL,
            AQI REAL
        );''')
    print("Database initialized")

# Load the pre-trained model
model = joblib.load(MODEL_PATH)
print("Model loaded successfully")

# Function to define sub-index calculation
def get_subindex(x):
    if x <= 50:
        return x
    elif x <= 100:
        return 50 + (x - 50) / 50 * 50
    elif x <= 200:
        return 100 + (x - 100) / 100 * 50
    elif x <= 300:
        return 200 + (x - 200) / 100 * 100
    elif x <= 400:
        return 300 + (x - 300) / 100 * 100
    else:
        return 400 + (x - 400) / 500 * 100

# Function to calculate AQI
def calculate_AQI_from_values(gas_values):
    sub_indices = [get_subindex(gas_values[gas]) for gas in gas_values]
    return sum(sub_indices) / len(sub_indices)

@app.route('/store', methods=['POST'])
def store_data():
    # Get data from POST request
    PM25 = float(request.form['PM25'])
    PM10 = float(request.form['PM10'])
    SO2 = float(request.form['SO2'])
    NOx = float(request.form['NOx'])
    NH3 = float(request.form['NH3'])
    CO = float(request.form['CO'])
    O3 = float(request.form['O3'])
    print("Data received successfully")
    
    # Create a DataFrame to ensure correct feature names
    data = pd.DataFrame({
        'PM2.5': [PM25],
        'PM10': [PM10],
        'SO2': [SO2],
        'NOx': [NOx],
        'NH3': [NH3],
        'CO': [CO],
        'O3': [O3]
    })
    
    # Predict AQI using the pre-trained model
    AQI = model.predict(data)[0]
    
    # Calculate AQI from values
    gas_values = {
        'PM2.5': PM25,
        'PM10': PM10,
        'SO2': SO2,
        'NOx': NOx,
        'NH3': NH3,
        'CO': CO,
        'O3': O3
    }
    calculated_AQI = calculate_AQI_from_values(gas_values)
    
    # Get current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Store data in SQLite database
    with sqlite3.connect(DATABASE) as conn:
        cur = conn.cursor()
        cur.execute('''INSERT INTO aqi_data (
            timestamp, PM25, PM10, SO2, NOx, NH3, CO, O3, AQI
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (timestamp, PM25, PM10, SO2, NOx, NH3, CO, O3, calculated_AQI))
        conn.commit()
    print("Data stored in database")
    
    return jsonify({'Predicted_AQI': AQI, 'Calculated_AQI': calculated_AQI}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
