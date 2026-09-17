import pandas as pd
import os

USERS_FILE = os.path.join(os.path.dirname(__file__), "users.csv")

def get_all_users():
    if not os.path.exists(USERS_FILE):
        return pd.DataFrame()
    return pd.read_csv(USERS_FILE)

def authenticate_user(email, password):
    df = get_all_users()
    if df.empty:
        return None
    user_row = df[(df["email"].str.strip().str.lower() == email.strip().lower()) & (df["password"] == password)]
    if not user_row.empty:
        return user_row.iloc[0].to_dict()
    return None

def get_users_by_role(role=None):
    df = get_all_users()
    if df.empty:
        return []
    if role:
        df = df[df["role"] == role]
    return df["name"].tolist()

ROLE_PERMISSIONS = {
    "Administrator": ["view_all", "manage_users", "create_work_orders", "complete_work_orders", "manage_inventory", "retrain_models", "export_reports"],
    "Maintenance Engineer": ["view_all", "create_work_orders", "complete_work_orders", "submit_feedback", "export_reports"],
    "Reliability Engineer": ["view_all", "view_ai_analytics", "retrain_models", "export_reports"],
    "Port Operations Planner": ["view_all", "view_fleet_status", "export_reports"]
}

def check_permission(role, permission):
    allowed = ROLE_PERMISSIONS.get(role, [])
    return "view_all" in allowed or permission in allowed
