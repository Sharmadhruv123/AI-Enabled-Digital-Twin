import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)

NUM_CRANES = 5
ROWS_PER_CRANE = 3000   # 5 cranes → 15,000 rows

# ---------------- CRANE TABLE ----------------
cranes = []

for i in range(1, NUM_CRANES + 1):
    cranes.append([
        i,
        f"QC-{i:02}",
        random.choice(["Mundra Terminal", "Yard Zone", "Dock Area"]),
        "2018-01-01",
        "2025-12-01",
        random.randint(70, 95),
        "Running"
    ])

cranes_df = pd.DataFrame(cranes, columns=[
    "crane_id","crane_name","location","installation_date",
    "last_maintenance","health_score","status"
])

cranes_df.to_csv("cranes.csv", index=False)

# ---------------- SENSOR DATA ----------------
sensor_rows = []
ai_rows = []
work_orders = []

start_time = datetime.now()

sensor_id = 1
workorder_id = 5000

for crane_id in range(1, NUM_CRANES + 1):

    base_temp = np.random.uniform(55, 65)
    base_vibration = np.random.uniform(0.3, 0.5)
    runtime = 1000
    failure_point = random.randint(2000, ROWS_PER_CRANE)
    
    # Pre-calculate ambient temps (seasonal/daily cycle)
    ambient_temps = 25 + 10 * np.sin(np.linspace(0, 4 * np.pi, ROWS_PER_CRANE)) + np.random.normal(0, 1, ROWS_PER_CRANE)

    temp_history = []
    vib_history = []

    for t in range(ROWS_PER_CRANE):

        timestamp = start_time + timedelta(minutes=5*t)
        amb_temp = ambient_temps[t]

        # degradation + noise + environment
        noise_temp = np.random.normal(0, 0.5)
        temp = base_temp + (t * 0.01) + (amb_temp * 0.2) + noise_temp
        
        noise_vib = np.random.normal(0, 0.02)
        vibration = base_vibration + (t * 0.0002) + noise_vib
        
        # Add random spikes if near failure
        if (t / failure_point) > 0.8:
            if random.random() > 0.9:
                vibration += np.random.uniform(0.5, 1.5)

        load = np.random.uniform(15, 25)
        motor_current = 25 + (t * 0.005) + (load * 0.5) + np.random.normal(0, 1)

        runtime += random.randint(1, 3)

        # Rolling features (approximate for simulation)
        temp_history.append(temp)
        vib_history.append(vibration)
        
        if len(temp_history) > 10:
            temp_history.pop(0)
            vib_history.pop(0)
            
        temp_rolling_avg = np.mean(temp_history)
        vib_rolling_avg = np.mean(vib_history)

        # failure logic
        failure_risk = min(1, (t / failure_point))

        if failure_risk < 0.6:
            health = "Normal"
        elif failure_risk < 0.8:
            health = "Warning"
        elif failure_risk < 0.95:
            health = "High Risk"
        else:
            health = "Critical"

            # auto create work order
            if random.random() > 0.95: # don't spam work orders
                work_orders.append([
                    workorder_id,
                    crane_id,
                    "Gearbox",
                    "High",
                    "High Vibration",
                    "Open",
                    timestamp.date(),
                    ""
                ])
                workorder_id += 1

        RUL = max(0, failure_point - t)

        sensor_rows.append([
            sensor_id, crane_id, temp, vibration, load,
            motor_current, runtime, timestamp, amb_temp
        ])

        ai_rows.append([
            temp, vibration, load, motor_current,
            runtime, amb_temp, temp_rolling_avg, vib_rolling_avg,
            RUL, failure_risk, health
        ])

        sensor_id += 1

# save sensor data
sensor_df = pd.DataFrame(sensor_rows, columns=[
    "sensor_id","crane_id","temperature","vibration",
    "load_tons","motor_current","runtime_hours","timestamp", "ambient_temp"
])

sensor_df.to_csv("sensor_data.csv", index=False)

# save AI training data
ai_df = pd.DataFrame(ai_rows, columns=[
    "temperature","vibration","load_tons",
    "motor_current","runtime_hours", "ambient_temp",
    "temp_rolling_avg", "vib_rolling_avg",
    "RUL","failure_risk","health_label"
])

ai_df.to_csv("ai_training_data.csv", index=False)

# ---------------- WORK ORDERS ----------------
work_df = pd.DataFrame(work_orders, columns=[
    "workorder_id","crane_id","component","priority",
    "issue_type","status","scheduled_date","completion_date"
])

work_df.to_csv("work_orders.csv", index=False)

# ---------------- SPARE PARTS ----------------
spare_parts = pd.DataFrame([
    [201,"Gearbox","Mechanical",5,2,2,120000],
    [202,"Wire Rope","Mechanical",12,4,5,15000],
    [203,"Brake Pad","Mechanical",20,3,6,4000],
    [204,"Temperature Sensor","Electrical",18,2,5,2500]
], columns=[
    "part_id","part_name","category",
    "stock_qty","reserved_qty","reorder_level","unit_cost"
])

spare_parts.to_csv("spare_parts.csv", index=False)

print("✅ All datasets generated successfully")