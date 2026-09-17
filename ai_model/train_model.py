import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import classification_report, mean_absolute_error, r2_score
import joblib
import os

# Set seed for reproducibility
RANDOM_STATE = 42

# Load dataset
data_path = os.path.join(os.path.dirname(__file__), "..", "ai_training_data.csv")
df = pd.read_csv(data_path)

# Features
features = [
    "temperature", "vibration", "load_tons", "motor_current", 
    "runtime_hours", "ambient_temp", "temp_rolling_avg", "vib_rolling_avg"
]
X = df[features]

# Labels
y_health = df["health_label"]
y_rul = df["RUL"]

# Split
print("Splitting data into training and testing sets...")
X_train, X_test, y_h_train, y_h_test, y_r_train, y_r_test = train_test_split(
    X, y_health, y_rul, test_size=0.2, random_state=RANDOM_STATE
)

# 1. Health Classification Model
print("\nTraining Health Classification Model (predicting sensor health status)...")
health_model = RandomForestClassifier(n_estimators=150, max_depth=12, random_state=RANDOM_STATE)
health_model.fit(X_train, y_h_train)

# 2. RUL Regression Model
print("Training RUL Regression Model (predicting Remaining Useful Life)...")
rul_model = RandomForestRegressor(n_estimators=150, max_depth=15, random_state=RANDOM_STATE)
rul_model.fit(X_train, y_r_train)

# Evaluation
print("\n" + "="*50)
print("EVALUATION RESULTS")
print("="*50)

y_h_pred = health_model.predict(X_test)
print("\nHealth Classification Performance:")
print(classification_report(y_h_test, y_h_pred))

y_r_pred = rul_model.predict(X_test)
print("\nRUL Regression Performance:")
print(f"Mean Absolute Error: {mean_absolute_error(y_r_test, y_r_pred):.2f} hours")
print(f"R2 Score (Variance Explained): {r2_score(y_r_test, y_r_pred):.4f}")

# Save models
save_path = os.path.join(os.path.dirname(__file__), "saved_model")
os.makedirs(save_path, exist_ok=True)

print(f"\nSaving results to {save_path}...")
joblib.dump(health_model, os.path.join(save_path, "health_model.pkl"))
joblib.dump(rul_model, os.path.join(save_path, "rul_model.pkl"))
joblib.dump(features, os.path.join(save_path, "features.pkl"))

print("\n✅ Advanced AI Training Complete!")