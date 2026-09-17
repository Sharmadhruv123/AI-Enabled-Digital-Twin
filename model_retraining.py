import pandas as pd
import numpy as np
import os
import pickle
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, IsolationForest
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, mean_absolute_error

ROOT_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(ROOT_DIR, "ai_model", "saved_model")
DATA_FILE = os.path.join(ROOT_DIR, "sensor_data.csv")
RETRAIN_FILE = os.path.join(ROOT_DIR, "model_retraining.csv")

FEATURES = [
    "temperature", "vibration", "load", "motor_current",
    "hydraulic_pressure", "runtime_hours", "ambient_temperature",
    "temp_rolling_avg", "vib_rolling_avg"
]

def train_or_retrain_models():
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    print("[AI PIPELINE] Loading sensor dataset for model training...")
    df = pd.read_csv(DATA_FILE)

    # 1. Feature Preprocessing
    scaler = StandardScaler()
    X = scaler.fit_transform(df[FEATURES])

    le = LabelEncoder()
    y_health = le.fit_transform(df["health_label"])
    y_rul = df["RUL"].values

    # 2. Train Classifier (Health State)
    clf = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
    clf.fit(X, y_health)
    health_preds = clf.predict(X)
    acc = accuracy_score(y_health, health_preds)

    # 3. Train Regressor (RUL in Hours)
    reg = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42)
    reg.fit(X, y_rul)
    rul_preds = reg.predict(X)
    mae = mean_absolute_error(y_rul, rul_preds)

    # 4. Train Isolation Forest (Anomaly Detection)
    iso = IsolationForest(contamination=0.05, random_state=42)
    iso.fit(X)

    # 5. Save Artifacts
    with open(os.path.join(MODEL_DIR, "scaler.pkl"), "wb") as f:
        pickle.dump(scaler, f)
    with open(os.path.join(MODEL_DIR, "label_encoder.pkl"), "wb") as f:
        pickle.dump(le, f)
    with open(os.path.join(MODEL_DIR, "health_clf.pkl"), "wb") as f:
        pickle.dump(clf, f)
    with open(os.path.join(MODEL_DIR, "rul_reg.pkl"), "wb") as f:
        pickle.dump(reg, f)
    with open(os.path.join(MODEL_DIR, "iso_forest.pkl"), "wb") as f:
        pickle.dump(iso, f)

    # 6. Log Retraining Record
    score_str = f"Accuracy: {acc*100:.1f}%, RUL MAE: {mae:.1f} hrs"
    print(f"[SUCCESS] Model Retraining Complete! Score: {score_str}")

    if os.path.exists(RETRAIN_FILE):
        retrain_df = pd.read_csv(RETRAIN_FILE)
    else:
        columns = ["retrain_id", "model_name", "training_data_from", "training_data_to", "algorithm", "parameters", "retrain_date", "model_version", "performance_score", "status"]
        retrain_df = pd.DataFrame(columns=columns)

    version_num = len(retrain_df) + 1
    new_record = {
        "retrain_id": f"RTN-{version_num:03d}",
        "model_name": "Crane_MultiOutput_Predictor",
        "training_data_from": df["timestamp"].min(),
        "training_data_to": df["timestamp"].max(),
        "algorithm": "RandomForest Classifier/Regressor + Isolation Forest",
        "parameters": "n_estimators=100, max_depth=10",
        "retrain_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "model_version": f"v1.{version_num}.0",
        "performance_score": score_str,
        "status": "Active"
    }

    retrain_df = pd.concat([retrain_df, pd.DataFrame([new_record])], ignore_index=True)
    retrain_df.to_csv(RETRAIN_FILE, index=False)
    return score_str

if __name__ == "__main__":
    train_or_retrain_models()
