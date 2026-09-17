import pandas as pd
import os
from datetime import datetime

FEEDBACK_FILE = os.path.join(os.path.dirname(__file__), "maintenance_feedback.csv")

def get_feedback():
    if not os.path.exists(FEEDBACK_FILE):
        return pd.DataFrame()
    return pd.read_csv(FEEDBACK_FILE)

def submit_feedback(work_order_id, crane_id, findings, actions_taken, condition_after, repair_duration_hours, notes=""):
    if os.path.exists(FEEDBACK_FILE):
        df = pd.read_csv(FEEDBACK_FILE)
    else:
        columns = ["feedback_id", "work_order_id", "crane_id", "feedback_date", "findings", "actions_taken", "condition_after", "repair_duration_hours", "notes"]
        df = pd.DataFrame(columns=columns)

    new_id = f"FBK-{len(df)+1:03d}"
    entry = {
        "feedback_id": new_id,
        "work_order_id": int(work_order_id),
        "crane_id": crane_id,
        "feedback_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "findings": findings,
        "actions_taken": actions_taken,
        "condition_after": condition_after,
        "repair_duration_hours": float(repair_duration_hours),
        "notes": notes
    }

    df = pd.concat([df, pd.DataFrame([entry])], ignore_index=True)
    df.to_csv(FEEDBACK_FILE, index=False)
    return new_id
