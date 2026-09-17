import pandas as pd
import numpy as np
import os

# Generate synthetic training data for crane predictive maintenance
np.random.seed(42)

n_samples = 1000

# Features: temperature, vibration, load_tons, motor_current, runtime_hours, ambient_temp, temp_rolling_avg, vib_rolling_avg
data = {
    "temperature": np.random.normal(75, 12, n_samples),  # Temperature in Celsius
    "vibration": np.random.exponential(0.8, n_samples),  # Vibration in mm/s
    "load_tons": np.random.uniform(10, 30, n_samples),  # Load in tons
    "motor_current": np.random.normal(40, 10, n_samples),  # Current in Amperes
    "runtime_hours": np.random.uniform(100, 5000, n_samples),  # Runtime hours
    "ambient_temp": np.random.uniform(15, 35, n_samples),  # Ambient temperature
    "temp_rolling_avg": np.random.normal(75, 12, n_samples),  # Rolling average of temperature
    "vib_rolling_avg": np.random.exponential(0.8, n_samples),  # Rolling average of vibration
}

# Generate labels based on sensor readings
# Health label: Normal, Warning, High Risk, Critical
health_labels = []
rul_values = []

for i in range(n_samples):
    temp = data["temperature"][i]
    vib = data["vibration"][i]
    current = data["motor_current"][i]
    runtime = data["runtime_hours"][i]
    
    # Health classification logic
    if temp < 60 and vib < 0.5 and current < 30:
        health = "Normal"
        rul = np.random.uniform(3000, 5000)
    elif temp < 80 and vib < 1.0 and current < 45:
        health = "Normal"
        rul = np.random.uniform(2500, 4000)
    elif temp < 85 and vib < 1.5 and current < 50:
        health = "Warning"
        rul = np.random.uniform(1000, 2500)
    elif temp < 90 and vib < 2.0:
        health = "High Risk"
        rul = np.random.uniform(500, 1500)
    else:
        health = "Critical"
        rul = np.random.uniform(50, 800)
    
    # Add runtime correlation to RUL (more runtime = less RUL remaining)
    rul = max(50, rul - (runtime / 1000))
    
    health_labels.append(health)
    rul_values.append(rul)

data["health_label"] = health_labels
data["RUL"] = rul_values

df = pd.DataFrame(data)

# Save to CSV
csv_path = os.path.join(os.path.dirname(__file__), "ai_training_data.csv")
df.to_csv(csv_path, index=False)

print(f"✅ Generated synthetic training data: {csv_path}")
print(f"Total samples: {len(df)}")
print(f"\nData preview:")
print(df.head())
print(f"\nHealth label distribution:")
print(df["health_label"].value_counts())
