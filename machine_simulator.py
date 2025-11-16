import time
import random
import joblib
import pandas as pd
import requests

# -------------------------------
# Load trained model
# -------------------------------
model = joblib.load("machine_failure_model.pkl")

# -------------------------------
# Endpoint to send POST alerts
# -------------------------------
ENDPOINT = "https://romanberg.app.n8n.cloud/webhook/machine-status"

# -------------------------------
# Function to generate synthetic data
# -------------------------------
def generate_machine_data():
    air_temp = round(random.uniform(290, 310), 1)          # Kelvin
    process_temp = round(air_temp + random.uniform(5, 20), 1)
    rotational_speed = random.randint(1200, 3000)          # rpm
    torque = round(random.uniform(10, 80), 1)              # Nm
    tool_wear = random.randint(0, 250)                     # minutes
    machine_type = random.choice(["L", "M", "H"])

    temp_diff = round(process_temp - air_temp, 1)

    return pd.DataFrame([{
        "Air temperature [K]": air_temp,
        "Process temperature [K]": process_temp,
        "Rotational speed [rpm]": rotational_speed,
        "Torque [Nm]": torque,
        "Tool wear [min]": tool_wear,
        "Type": machine_type,
        "Temperature Difference [K]": temp_diff
    }])


# -------------------------------
# Main Loop
# -------------------------------
print("Machine simulator started. Sending data every 60 seconds...\n")

while True:
    # Generate realistic synthetic machine telemetry
    name = f"Machine{random.randint(0, 100)}"
    data = generate_machine_data()

    # Run prediction
    prediction = int(model.predict(data)[0])                    # 0 or 1
    probability = float(model.predict_proba(data)[0][1])        # failure likelihood

    # Prepare JSON
    payload = {
        "Name": name,         # 0 = OK, 1 = failure
        "Machine Fail": probability,       # Failure likelihood
    }

    # Display locally
    print("\nGenerated Machine Data:")
    print(payload)

    # Send POST request
    try:
        response = requests.post(ENDPOINT, json=payload, timeout=5)
        print("POST Status:", response.status_code)
    except Exception as e:
        print("POST Failed:", e)

    # Wait 60 seconds
    time.sleep(10)
