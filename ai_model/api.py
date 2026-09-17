from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os

app = FastAPI(title="Crane Predictive Maintenance API")

# Allow frontend/backend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths
MODELS_DIR = os.path.join(os.path.dirname(__file__), "saved_model")

# Load models and features
try:
    health_model = joblib.load(os.path.join(MODELS_DIR, "health_model.pkl"))
    rul_model = joblib.load(os.path.join(MODELS_DIR, "rul_model.pkl"))
    model_features = joblib.load(os.path.join(MODELS_DIR, "features.pkl"))
    print("✅ All models and feature mappings loaded successfully")
except Exception as e:
    print(f"❌ Error loading models: {e}")
    health_model = None
    rul_model = None
    model_features = []

class PredictionInput(BaseModel):
    temperature: float
    vibration: float
    load_tons: float
    motor_current: float
    runtime_hours: float
    ambient_temp: float = 25.0
    temp_rolling_avg: float = None
    vib_rolling_avg: float = None

@app.get("/")
def home():
    return {
        "status": "online",
        "service": "Crane Predictive Maintenance AI",
        "models_loaded": health_model is not None and rul_model is not None,
        "features_required": model_features
    }

@app.post("/predict")
def predict(data: PredictionInput):
    if health_model is None or rul_model is None:
        raise HTTPException(status_code=503, detail="Models not loaded")

    try:
        # Prepare input data
        input_dict = data.dict()
        
        # Handle defaults for rolling features if not provided
        if input_dict["temp_rolling_avg"] is None:
            input_dict["temp_rolling_avg"] = input_dict["temperature"]
        if input_dict["vib_rolling_avg"] is None:
            input_dict["vib_rolling_avg"] = input_dict["vibration"]

        # Create DataFrame with exact feature order
        df = pd.DataFrame([input_dict])[model_features]

        # 1. Health Prediction (Label + Probabilities)
        health_labels = health_model.classes_
        health_probs = health_model.predict_proba(df)[0]
        health_pred = health_model.predict(df)[0]
        
        confidence = float(np.max(health_probs))
        
        # 2. RUL Prediction
        rul_pred = float(rul_model.predict(df)[0])

        # Risk Score Calculation (Composite)
        # Higher risk if health is not Normal OR RUL is low
        risk_score = 0
        if health_pred == "Warning": risk_score = 40
        elif health_pred == "High Risk": risk_score = 75
        elif health_pred == "Critical": risk_score = 100
        
        # Adjust risk based on RUL (assuming < 100 hours is critical)
        if rul_pred < 100:
            risk_score = max(risk_score, 90)
        elif rul_pred < 500:
            risk_score = max(risk_score, 50)

        # Detailed Issue Diagnostic
        issue_description = "All systems operating within normal parameters."
        if health_pred == "Warning":
            if data.vibration > 0.7:
                issue_description = "Slight vibration anomaly detected in main hoist motor."
            elif data.temperature > 82:
                issue_description = "Temperature rising above optimal levels. Thermal stress suspected."
            else:
                issue_description = "General wear-and-tear detected. Schedule routine check."
        elif health_pred in ["High Risk", "Critical"]:
            if data.vibration > 1.8:
                issue_description = "SEVERE VIBRATION SPIKE. Potential bearing failure in trolley drive."
            elif data.temperature > 90:
                issue_description = "CRITICAL TEMPERATURE SHOT. Overheating in motor control unit."
            else:
                issue_description = "Multiple sensor anomalies. High risk of immediate downtime."

        return {
            "health_status": str(health_pred),
            "confidence": round(confidence, 4),
            "estimated_rul_hours": round(rul_pred, 1),
            "risk_score": risk_score,
            "maintenance_recommendation": "Immediate Inspection" if risk_score > 70 else "Schedule Soon" if risk_score > 40 else "Routine",
            "issue_description": issue_description
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)