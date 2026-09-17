import pandas as pd
import numpy as np
import os
import pickle

ROOT_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(ROOT_DIR, "ai_model", "saved_model")
DATA_FILE = os.path.join(ROOT_DIR, "sensor_data.csv")

FEATURES = [
    "temperature", "vibration", "load", "motor_current",
    "hydraulic_pressure", "runtime_hours", "ambient_temperature",
    "temp_rolling_avg", "vib_rolling_avg"
]

class PredictionPipeline:
    def __init__(self):
        with open(os.path.join(MODEL_DIR, "scaler.pkl"), "rb") as f:
            self.scaler = pickle.load(f)
        with open(os.path.join(MODEL_DIR, "label_encoder.pkl"), "rb") as f:
            self.le = pickle.load(f)
        with open(os.path.join(MODEL_DIR, "health_clf.pkl"), "rb") as f:
            self.clf = pickle.load(f)
        with open(os.path.join(MODEL_DIR, "rul_reg.pkl"), "rb") as f:
            self.reg = pickle.load(f)
        with open(os.path.join(MODEL_DIR, "iso_forest.pkl"), "rb") as f:
            self.iso = pickle.load(f)

    def predict_sample(self, sample_dict):
        # Format input dataframe
        df_input = pd.DataFrame([sample_dict])
        for feat in FEATURES:
            if feat not in df_input.columns:
                df_input[feat] = 0.0

        X = self.scaler.transform(df_input[FEATURES])

        # Predictions
        health_idx = self.clf.predict(X)[0]
        health_status = self.le.inverse_transform([health_idx])[0]
        health_probs = self.clf.predict_proba(X)[0]
        confidence = float(np.max(health_probs))

        rul_val = int(max(0, self.reg.predict(X)[0]))

        iso_val = self.iso.decision_function(X)[0]
        is_anomaly = bool(iso_val < 0)
        anomaly_score = float(max(0.0, -iso_val * 2.5))

        # Health Index Score (0 to 100%)
        vib = float(sample_dict.get("vibration", 0.3))
        temp = float(sample_dict.get("temperature", 60))
        current = float(sample_dict.get("motor_current", 30))

        vib_penalty = min(40, max(0, (vib - 0.5) * 20))
        temp_penalty = min(40, max(0, (temp - 70) * 1.5))
        current_penalty = min(20, max(0, (current - 45) * 0.8))

        health_score = max(5.0, round(100.0 - (vib_penalty + temp_penalty + current_penalty), 1))
        failure_prob = round(100.0 - health_score, 1)

        # AI Recommendation & Issue Diagnosis
        if health_status == "Critical" or vib > 2.0 or temp > 90:
            issue = "Critical Gearbox/Motor Strain" if temp > 85 else "Severe Mechanical Vibration"
            recommendation = "EMERGENCY: Immediate shutdown and work order creation required. Inspect bearing sets and hydraulic pump."
        elif health_status == "High Risk" or vib > 1.2 or temp > 80:
            issue = "High Bearing Wear & Elevated Temperature"
            recommendation = "Schedule urgent maintenance within 24 hours. Check lubrication and wire rope tension."
        elif health_status == "Warning" or vib > 0.8 or temp > 72:
            issue = "Moderate Thermal/Vibrational Drift"
            recommendation = "Monitor telemetry closely. Plan routine preventive maintenance during next operational window."
        else:
            issue = "All Subsystems Operational"
            recommendation = "Equipment operating within optimal parameters. Continue regular monitoring."

        return {
            "health_status": health_status,
            "confidence": confidence,
            "estimated_rul": rul_val,
            "is_anomaly": is_anomaly,
            "anomaly_score": round(anomaly_score, 4),
            "health_score": health_score,
            "failure_probability": failure_prob,
            "issue": issue,
            "recommendation": recommendation
        }

    def predict_latest_for_crane(self, crane_id):
        if not os.path.exists(DATA_FILE):
            return None
        df = pd.read_csv(DATA_FILE)
        crane_rows = df[df["crane_id"] == crane_id]
        if crane_rows.empty:
            return None
        latest_sample = crane_rows.iloc[-1].to_dict()
        res = self.predict_sample(latest_sample)
        res["latest_sensor"] = latest_sample
        return res

pipeline_instance = None
def get_pipeline():
    global pipeline_instance
    if pipeline_instance is None:
        pipeline_instance = PredictionPipeline()
    return pipeline_instance
