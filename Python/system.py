import serial
import time
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib
import os

ARDUINO_PORT = 'COM3' 
BAUD_RATE = 9600
MODEL_FILE = 'obstacle_model.pkl'
DATA_FILE = '../data/labeled_data.csv' 

# ----- Load or Train Model -----
if os.path.exists(MODEL_FILE):
    print("Loading existing model...")
    model = joblib.load(MODEL_FILE)
else:
    print("Training new model from data...")
    # Load dataset
    df = pd.read_csv(DATA_FILE)
    X = df[['ldr_value', 'ir_value']].values
    y = df['label'].values
    
   
    model = DecisionTreeClassifier()
    model.fit(X, y)
    
    
    joblib.dump(model, MODEL_FILE)
    print("Model trained and saved!")

print("Connecting to Arduino...")
arduino = serial.Serial(port=ARDUINO_PORT, baudrate=BAUD_RATE, timeout=1)
time.sleep(2)
print("Connected.")

print("Starting obstacle detection...")
while True:
    try:
        if arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').strip()
            if line:
                # Expecting: "ldr: <value> ir: <value>"
                parts = line.split()
                if len(parts) >= 4:
                    ldr_value = int(parts[1])
                    ir_value = int(parts[3])
                    
                    data = np.array([[ldr_value, ir_value]])
                    prediction = model.predict(data)[0]
                    
                    status = "Obstacle Detected!" if prediction == 1 else "No Obstacle"
                    print(f"LDR={ldr_value}, IR={ir_value} -> {status}")
    except Exception as e:
        print("Error:", e)
