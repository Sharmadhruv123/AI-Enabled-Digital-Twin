import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import random

# Set random seed
np.random.seed(42)
random.seed(42)

# Configuration - Saving to Root
ROOT_DIR = os.path.dirname(__file__)
NUM_CRANES = 10
ROWS_PER_CRANE = 1000

# 1. CRANE MASTER DATA
locations = ["Singapore Port", "Dubai Jebel Ali", "Rotterdam Terminal", "Shanghai Yard", "Mumbai Port"]
cranes = []
for i in range(1, NUM_CRANES + 1):
    install_date = datetime.now() - timedelta(days=random.randint(365, 365*5))
    cranes.append({
        "crane_id": f"CRN-{i:03}",
        "location": random.choice(locations),
        "installation_date": install_date.strftime("%Y-%m-%d"),
        "health_score": random.randint(85, 100),
        "status": "Running"
    })

pd.DataFrame(cranes).to_csv(os.path.join(ROOT_DIR, "cranes.csv"), index=False)

# 2. SENSOR DATA GENERATION
sensor_data_list = []
start_time = datetime.now() - timedelta(days=30)

for crane in cranes:
    crane_id = crane["crane_id"]
    base_temp = np.random.uniform(50, 65)
    base_vibration = np.random.uniform(0.1, 0.4)
    failure_point = random.randint(int(ROWS_PER_CRANE * 0.7), ROWS_PER_CRANE)
    
    for t in range(ROWS_PER_CRANE):
        timestamp = start_time + timedelta(hours=t)
        degradation = (t / ROWS_PER_CRANE) ** 2
        amb_temp = 25 + 5 * np.sin(2 * np.pi * t / 24) + np.random.normal(0, 0.2)
        
        temp = base_temp + (degradation * 30) + (amb_temp * 0.1) + np.random.normal(0, 0.5)
        vibration = base_vibration + (degradation * 1.5) + np.random.normal(0, 0.05)
        
        if t > failure_point - 50 and random.random() > 0.8:
            vibration += np.random.uniform(0.5, 2.0)
            temp += np.random.uniform(2, 10)
        
        load = np.random.uniform(10, 40)
        motor_current = 20 + (load * 0.8) + (vibration * 5) + np.random.normal(0, 1)
        
        health_ratio = t / failure_point
        if health_ratio < 0.6: health, rul = "Normal", failure_point - t + random.randint(0, 100)
        elif health_ratio < 0.8: health, rul = "Warning", failure_point - t + random.randint(0, 50)
        elif health_ratio < 0.95: health, rul = "High Risk", max(0, failure_point - t + random.randint(0, 20))
        else: health, rul = "Critical", max(0, failure_point - t)

        sensor_data_list.append({
            "crane_id": crane_id, "timestamp": timestamp, "temperature": round(temp, 2),
            "vibration": round(vibration, 3), "load": round(load, 2),
            "motor_current": round(motor_current, 2), "runtime_hours": round(t * 1.2, 1),
            "ambient_temperature": round(amb_temp, 2), "health_label": health, "RUL": int(rul)
        })

sensor_df = pd.DataFrame(sensor_data_list)
sensor_df["temp_rolling_avg"] = sensor_df.groupby("crane_id")["temperature"].transform(lambda x: x.rolling(window=10, min_periods=1).mean())
sensor_df["vib_rolling_avg"] = sensor_df.groupby("crane_id")["vibration"].transform(lambda x: x.rolling(window=10, min_periods=1).mean())

sensor_df.to_csv(os.path.join(ROOT_DIR, "sensor_data.csv"), index=False)
# Compatibility with existing AI training scripts
sensor_df.to_csv(os.path.join(ROOT_DIR, "ai_training_data.csv"), index=False)

# 3. ERP / INVENTORY DATA
inventory = [
    {"part_name": "Hydraulic Pump", "stock_qty": 5, "reserved_qty": 0, "reorder_level": 2, "cost": 1200},
    {"part_name": "Wire Rope (50m)", "stock_qty": 10, "reserved_qty": 0, "reorder_level": 3, "cost": 450},
    {"part_name": "Brake Lining", "stock_qty": 15, "reserved_qty": 0, "reorder_level": 5, "cost": 150},
    {"part_name": "Bearing Set", "stock_qty": 8, "reserved_qty": 0, "reorder_level": 2, "cost": 300},
    {"part_name": "Control PCBA", "stock_qty": 3, "reserved_qty": 0, "reorder_level": 1, "cost": 2500},
    {"part_name": "Oil Filter", "stock_qty": 20, "reserved_qty": 0, "reorder_level": 10, "cost": 25}
]
pd.DataFrame(inventory).to_csv(os.path.join(ROOT_DIR, "spare_parts.csv"), index=False)

# 4. CMMS (Empty initial work orders)
columns = ["work_order_id", "crane_id", "issue", "priority", "action", "status", "created_at", "assigned_parts", "total_cost"]
pd.DataFrame(columns=columns).to_csv(os.path.join(ROOT_DIR, "work_orders.csv"), index=False)

print("[DONE] Integrated datasets generated successfully in root.")
