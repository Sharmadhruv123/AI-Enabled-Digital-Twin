import joblib
import pandas as pd
import os

# Paths
MODELS_DIR = os.path.join(os.path.dirname(__file__), "saved_model")

# Load models and features
health_model = joblib.load(os.path.join(MODELS_DIR, "health_model.pkl"))
rul_model = joblib.load(os.path.join(MODELS_DIR, "rul_model.pkl"))
model_features = joblib.load(os.path.join(MODELS_DIR, "features.pkl"))

def test_prediction(temp, vib, load, current, runtime, amb=25.0):
    sample = pd.DataFrame([{
        "temperature": temp,
        "vibration": vib,
        "load_tons": load,
        "motor_current": current,
        "runtime_hours": runtime,
        "ambient_temp": amb,
        "temp_rolling_avg": temp, # assume same for single test
        "vib_rolling_avg": vib
    }])
    
    # Reorder columns
    sample = sample[model_features]
    
    health = health_model.predict(sample)[0]
    rul = rul_model.predict(sample)[0]
    
    print(f"\n--- Prediction for {temp}°C, {vib}mm/s ---")
    print(f"Predicted Health: {health}")
    print(f"Estimated RUL: {rul:.1f} hours")

# Test 1: Normal
test_prediction(65, 0.4, 20, 35, 1200)

# Test 2: Warning (Higher temp/vib)
test_prediction(85, 1.2, 22, 48, 2500)

# Test 3: Critical (Very high vib)
test_prediction(92, 2.8, 24, 55, 2900)