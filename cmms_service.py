import pandas as pd
import os
from datetime import datetime

DATA_FILE = os.path.join(os.path.dirname(__file__), "work_orders.csv")

def get_work_orders(crane_id=None, status=None):
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame()
    df = pd.read_csv(DATA_FILE)
    if crane_id:
        df = df[df["crane_id"] == crane_id]
    if status:
        df = df[df["status"] == status]
    return df

def create_work_order(crane_id, issue, priority, action, assigned_parts, total_cost, technician="Rajesh Kumar"):
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        columns = ["work_order_id", "crane_id", "issue", "priority", "action", "status", "created_at", "closed_at", "assigned_parts", "total_cost", "assigned_technician"]
        df = pd.DataFrame(columns=columns)
    
    new_id = 5000 + len(df) + 1
    new_wo = {
        "work_order_id": new_id,
        "crane_id": crane_id,
        "issue": issue,
        "priority": priority,
        "action": action,
        "status": "Open",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "closed_at": "",
        "assigned_parts": assigned_parts,
        "total_cost": float(total_cost),
        "assigned_technician": technician
    }
    
    df = pd.concat([df, pd.DataFrame([new_wo])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    return new_id

def update_work_order_status(wo_id, new_status, technician=None):
    if not os.path.exists(DATA_FILE):
        return False
    df = pd.read_csv(DATA_FILE)
    if wo_id in df["work_order_id"].values:
        df.loc[df["work_order_id"] == wo_id, "status"] = new_status
        if new_status == "Completed":
            df.loc[df["work_order_id"] == wo_id, "closed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        if technician:
            df.loc[df["work_order_id"] == wo_id, "assigned_technician"] = technician
        df.to_csv(DATA_FILE, index=False)
        return True
    return False
