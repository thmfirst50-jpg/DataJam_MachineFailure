import joblib
import pandas as pd
import requests

# Load the model
model = joblib.load("machine_failure_model.pkl")

# Test Data
new_data = pd.DataFrame([{
    "Air temperature [K]": 300,
    "Process temperature [K]": 310,
    "Rotational speed [rpm]": 1500,
    "Torque [Nm]": 65,
    "Tool wear [min]": 100,
    "Type": "L",
    "Temperature Difference [K]": 0
}])

# Predict
prediction = model.predict(new_data)[0]
probability = model.predict_proba(new_data)[0][1]

print("Failure prediction (0 = no, 1 = yes):", prediction)
print("Failure probability:", probability)


url = "https://romanberg.app.n8n.cloud/webhook-test/machine-status"

payload = {
    "Name": "Machine1",         # 0 = OK, 1 = failure
    "Machine Fail": probability,       # Failure likelihood
}

# If you need headers:
headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, json=payload, headers=headers)
    print("POST status:", response.status_code)
    print("Response:", response.text)
except Exception as e:
    print("POST request failed:", e)