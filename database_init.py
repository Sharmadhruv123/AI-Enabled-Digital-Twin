import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

ROOT_DIR = os.path.dirname(__file__)

def init_all_databases():
    print("Initializing Database Tables (10 ER Diagram Entities)...")

    # 1. Users
    users_file = os.path.join(ROOT_DIR, "users.csv")
    users_data = [
        {"user_id": "U-101", "name": "Sharma Dhruv", "email": "dhruv@port.com", "password": "admin", "role": "Administrator", "phone": "+91-9876543210", "status": "Active", "created_at": "2026-01-10 09:00"},
        {"user_id": "U-102", "name": "Rajesh Kumar", "email": "rajesh@port.com", "password": "engineer", "role": "Maintenance Engineer", "phone": "+91-9876543211", "status": "Active", "created_at": "2026-01-12 10:30"},
        {"user_id": "U-103", "name": "Ananya Roy", "email": "ananya@port.com", "password": "reliability", "role": "Reliability Engineer", "phone": "+91-9876543212", "status": "Active", "created_at": "2026-01-15 14:00"},
        {"user_id": "U-104", "name": "Vikram Singh", "email": "vikram@port.com", "password": "planner", "role": "Port Operations Planner", "phone": "+91-9876543213", "status": "Active", "created_at": "2026-01-20 11:15"}
    ]
    pd.DataFrame(users_data).to_csv(users_file, index=False)

    # 2. Cranes
    cranes_file = os.path.join(ROOT_DIR, "cranes.csv")
    cranes_data = [
        {"crane_id": "CR-001", "crane_name": "STS Super Crane 1", "crane_type": "Ship-to-Shore (STS)", "model": "ZPMC-STS-65T", "capacity_tons": 65, "location": "Terminal A - Berth 1", "manufacture_year": 2021, "status": "Running"},
        {"crane_id": "CR-002", "crane_name": "STS Super Crane 2", "crane_type": "Ship-to-Shore (STS)", "model": "ZPMC-STS-65T", "capacity_tons": 65, "location": "Terminal A - Berth 2", "manufacture_year": 2021, "status": "Running"},
        {"crane_id": "CR-003", "crane_name": "RTG Yard Crane 1", "crane_type": "Rubber-Tyred Gantry (RTG)", "model": "Kalmar-RTG-41T", "capacity_tons": 41, "location": "Container Yard Block C", "manufacture_year": 2022, "status": "Warning"},
        {"crane_id": "CR-004", "crane_name": "RMG Rail Crane 1", "crane_type": "Rail-Mounted Gantry (RMG)", "model": "Liebherr-RMG-50T", "capacity_tons": 50, "location": "Rail Terminal Block R1", "manufacture_year": 2020, "status": "Running"},
        {"crane_id": "CR-005", "crane_name": "RTG Yard Crane 2", "crane_type": "Rubber-Tyred Gantry (RTG)", "model": "Kalmar-RTG-41T", "capacity_tons": 41, "location": "Container Yard Block D", "manufacture_year": 2023, "status": "Critical"}
    ]
    pd.DataFrame(cranes_data).to_csv(cranes_file, index=False)

    # 3. Components
    components_file = os.path.join(ROOT_DIR, "components.csv")
    components_data = []
    subsystems = [
        ("Hoist Motor", "Electrical/Drive", "High"),
        ("Main Gearbox", "Mechanical Transmission", "Critical"),
        ("Wire Ropes & Drums", "Structural/Lifting", "Critical"),
        ("Trolley Drive System", "Mechanical Motion", "Medium"),
        ("Electrical Control Panel", "Power Distribution", "High"),
        ("Structural Load Cells", "Structural Sensing", "High")
    ]
    comp_idx = 1
    for crane in cranes_data:
        for comp_name, comp_type, criticality in subsystems:
            components_data.append({
                "component_id": f"CMP-{comp_idx:03d}",
                "crane_id": crane["crane_id"],
                "component_name": comp_name,
                "component_type": comp_type,
                "installation_date": "2023-03-15",
                "criticality": criticality,
                "status": "Operational" if crane["status"] == "Running" else crane["status"]
            })
            comp_idx += 1
    pd.DataFrame(components_data).to_csv(components_file, index=False)

    # 4. Spare Parts (ERP)
    spare_parts_file = os.path.join(ROOT_DIR, "spare_parts.csv")
    spare_parts_data = [
        {"spare_part_id": "SP-001", "part_name": "Bearing Set (Heavy Duty)", "part_number": "BRG-6320-C3", "category": "Mechanical", "stock_qty": 14, "reserved_qty": 2, "reorder_level": 5, "unit_price": 450.0, "status": "Available"},
        {"spare_part_id": "SP-002", "part_name": "Wire Rope (50m Galvanized)", "part_number": "WR-32MM-50M", "category": "Rigging", "stock_qty": 6, "reserved_qty": 1, "reorder_level": 3, "unit_price": 1200.0, "status": "Available"},
        {"spare_part_id": "SP-003", "part_name": "Synthetic Oil Filter", "part_number": "FLT-HYD-99", "category": "Hydraulics", "stock_qty": 25, "reserved_qty": 3, "reorder_level": 10, "unit_price": 85.0, "status": "Available"},
        {"spare_part_id": "SP-004", "part_name": "Hydraulic Pump Assembly", "part_number": "PMP-REX-250", "category": "Hydraulics", "stock_qty": 3, "reserved_qty": 1, "reorder_level": 2, "unit_price": 3100.0, "status": "Low Stock"},
        {"spare_part_id": "SP-005", "part_name": "Control PCBA Unit", "part_number": "PCB-ABB-800", "category": "Electronics", "stock_qty": 4, "reserved_qty": 0, "reorder_level": 2, "unit_price": 1850.0, "status": "Available"},
        {"spare_part_id": "SP-006", "part_name": "Brake Shoe Lining Set", "part_number": "BRK-SH-400", "category": "Braking", "stock_qty": 18, "reserved_qty": 0, "reorder_level": 5, "unit_price": 320.0, "status": "Available"}
    ]
    pd.DataFrame(spare_parts_data).to_csv(spare_parts_file, index=False)

    # 5. Sensor Data Generation
    sensor_file = os.path.join(ROOT_DIR, "sensor_data.csv")
    np.random.seed(42)
    rows = []
    base_time = datetime.now() - timedelta(days=30)
    
    for crane in cranes_data:
        c_id = crane["crane_id"]
        runtime = 1000.0
        for i in range(200):
            t_stamp = (base_time + timedelta(hours=i*3.6)).strftime("%Y-%m-%d %H:%M")
            runtime += 3.6
            
            # Simulate health progression
            if c_id == "CR-001":
                temp = 62.0 + np.random.normal(0, 1.5)
                vib = 0.35 + np.random.normal(0, 0.05)
                load = 22.0 + np.random.normal(0, 3.0)
                current = 32.0 + np.random.normal(0, 2.0)
                press = 150.0 + np.random.normal(0, 5.0)
                health = "Normal"
                rul = max(10, 1200 - i*5)
            elif c_id == "CR-003":
                temp = 78.0 + (i*0.08) + np.random.normal(0, 2.0)
                vib = 1.1 + (i*0.005) + np.random.normal(0, 0.08)
                load = 28.0 + np.random.normal(0, 2.5)
                current = 48.0 + np.random.normal(0, 3.0)
                press = 175.0 + np.random.normal(0, 6.0)
                health = "Warning" if i < 150 else "High Risk"
                rul = max(10, 800 - i*3.5)
            elif c_id == "CR-005":
                temp = 88.0 + (i*0.12) + np.random.normal(0, 2.5)
                vib = 2.3 + (i*0.01) + np.random.normal(0, 0.15)
                load = 34.0 + np.random.normal(0, 3.0)
                current = 62.0 + np.random.normal(0, 4.0)
                press = 210.0 + np.random.normal(0, 8.0)
                health = "High Risk" if i < 120 else "Critical"
                rul = max(5, 450 - i*2.2)
            else:
                temp = 60.0 + np.random.normal(0, 1.2)
                vib = 0.30 + np.random.normal(0, 0.04)
                load = 18.0 + np.random.normal(0, 2.0)
                current = 28.0 + np.random.normal(0, 1.5)
                press = 145.0 + np.random.normal(0, 4.0)
                health = "Normal"
                rul = max(10, 1500 - i*6)

            rows.append({
                "sensor_data_id": f"SD-{len(rows)+1:05d}",
                "crane_id": c_id,
                "component_id": f"CMP-{(hash(c_id)%6)+1:03d}",
                "timestamp": t_stamp,
                "temperature": round(max(30.0, temp), 2),
                "vibration": round(max(0.05, vib), 3),
                "load": round(max(5.0, load), 1),
                "motor_current": round(max(10.0, current), 1),
                "hydraulic_pressure": round(max(50.0, press), 1),
                "runtime_hours": round(runtime, 1),
                "ambient_temperature": round(28.0 + np.random.normal(0, 2.0), 1),
                "temp_rolling_avg": round(max(30.0, temp), 2),
                "vib_rolling_avg": round(max(0.05, vib), 3),
                "health_label": health,
                "RUL": int(max(0, rul))
            })
    pd.DataFrame(rows).to_csv(sensor_file, index=False)

    # 6. Work Orders (CMMS)
    work_orders_file = os.path.join(ROOT_DIR, "work_orders.csv")
    wo_data = [
        {"work_order_id": 5001, "crane_id": "CR-003", "issue": "High Gearbox Vibration & Heat", "priority": "High", "action": "Corrective Maintenance", "status": "In Progress", "created_at": "2026-09-12 10:00", "closed_at": "", "assigned_parts": "Bearing Set (Heavy Duty)", "total_cost": 450.0, "assigned_technician": "Rajesh Kumar"},
        {"work_order_id": 5002, "crane_id": "CR-005", "issue": "Critical Motor Current & Overheating", "priority": "Emergency", "action": "Corrective Maintenance", "status": "Open", "created_at": "2026-09-15 16:30", "closed_at": "", "assigned_parts": "Synthetic Oil Filter, Hydraulic Pump Assembly", "total_cost": 3185.0, "assigned_technician": "Rajesh Kumar"},
        {"work_order_id": 5003, "crane_id": "CR-001", "issue": "Routine Wire Rope Inspection", "priority": "Medium", "action": "Preventive Maintenance", "status": "Completed", "created_at": "2026-09-01 08:30", "closed_at": "2026-09-01 12:00", "assigned_parts": "Wire Rope (50m Galvanized)", "total_cost": 1200.0, "assigned_technician": "Vikram Singh"}
    ]
    pd.DataFrame(wo_data).to_csv(work_orders_file, index=False)

    # 7. Predictions
    predictions_file = os.path.join(ROOT_DIR, "predictions.csv")
    pred_data = [
        {"prediction_id": "PRD-001", "crane_id": "CR-003", "component_id": "CMP-014", "timestamp": "2026-09-16 11:00", "health_score": 62.5, "failure_probability": 37.5, "rul_hours": 320, "anomaly_score": 0.0842, "prediction_model": "Bi-LSTM + Isolation Forest", "status": "Logged"},
        {"prediction_id": "PRD-002", "crane_id": "CR-005", "component_id": "CMP-026", "timestamp": "2026-09-16 11:30", "health_score": 22.0, "failure_probability": 78.0, "rul_hours": 45, "anomaly_score": 0.2415, "prediction_model": "Bi-LSTM + Isolation Forest", "status": "Alert Triggered"}
    ]
    pd.DataFrame(pred_data).to_csv(predictions_file, index=False)

    # 8. Alerts
    alerts_file = os.path.join(ROOT_DIR, "alerts.csv")
    alerts_data = [
        {"alert_id": "ALT-001", "crane_id": "CR-003", "prediction_id": "PRD-001", "alert_type": "Vibration Warning", "severity": "High", "message": "Gearbox vibration exceeded threshold (1.45 mm/s).", "alert_time": "2026-09-16 11:02", "status": "Acknowledged", "acknowledged_by": "Rajesh Kumar", "acknowledged_at": "2026-09-16 11:15"},
        {"alert_id": "ALT-002", "crane_id": "CR-005", "prediction_id": "PRD-002", "alert_type": "Motor Overheat Critical", "severity": "Critical", "message": "Hoist motor temp reached 94.2°C. Immediate action required.", "alert_time": "2026-09-16 11:31", "status": "New", "acknowledged_by": "", "acknowledged_at": ""}
    ]
    pd.DataFrame(alerts_data).to_csv(alerts_file, index=False)

    # 9. Maintenance Feedback (Closed-Loop)
    feedback_file = os.path.join(ROOT_DIR, "maintenance_feedback.csv")
    feedback_data = [
        {"feedback_id": "FBK-001", "work_order_id": 5003, "crane_id": "CR-001", "feedback_date": "2026-09-01 12:15", "findings": "Minor surface wear on wire rope strands. Replaced per safety schedule.", "actions_taken": "Replaced wire rope, lubricated drum sheaves, recalibrated tension sensor.", "condition_after": "Normal", "repair_duration_hours": 3.5, "notes": "No structural defects found on sheaves."}
    ]
    pd.DataFrame(feedback_data).to_csv(feedback_file, index=False)

    # 10. Model Retraining History
    retrain_file = os.path.join(ROOT_DIR, "model_retraining.csv")
    retrain_data = [
        {"retrain_id": "RTN-001", "model_name": "Crane_BiLSTM_Health_Predictor_v1.0", "training_data_from": "2026-08-01", "training_data_to": "2026-08-31", "algorithm": "RandomForest + MLP Ensemble", "parameters": "n_estimators=100, max_depth=12", "retrain_date": "2026-09-01 02:00", "model_version": "v1.0.0", "performance_score": "Accuracy: 94.8%, RUL MAE: 18.2 hrs", "status": "Active"}
    ]
    pd.DataFrame(retrain_data).to_csv(retrain_file, index=False)

    print("[SUCCESS] All 10 Database Tables Successfully Created!")

if __name__ == "__main__":
    init_all_databases()
