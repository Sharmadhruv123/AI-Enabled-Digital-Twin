import pandas as pd
import os

INVENTORY_FILE = os.path.join(os.path.dirname(__file__), "spare_parts.csv")

ISSUE_PARTS_MAPPING = {
    "High Gearbox Vibration & Heat": ["Bearing Set (Heavy Duty)", "Synthetic Oil Filter"],
    "Critical Motor Current & Overheating": ["Synthetic Oil Filter", "Hydraulic Pump Assembly"],
    "High Vibration": ["Bearing Set (Heavy Duty)", "Wire Rope (50m Galvanized)"],
    "Overheating": ["Synthetic Oil Filter", "Hydraulic Pump Assembly"],
    "Structural Wear": ["Wire Rope (50m Galvanized)"],
    "Electrical Fault": ["Control PCBA Unit"],
    "Brake Wear": ["Brake Shoe Lining Set"],
    "General Maintenance": ["Synthetic Oil Filter"]
}

def get_inventory():
    if not os.path.exists(INVENTORY_FILE):
        return pd.DataFrame()
    return pd.read_csv(INVENTORY_FILE)

def check_and_reserve_parts(issue):
    df = get_inventory()
    if df.empty:
        return False, "", 0.0, "Inventory database not found."
    
    needed_parts = ISSUE_PARTS_MAPPING.get(issue, ["Synthetic Oil Filter"])
    parts_to_reserve = []
    total_cost = 0.0
    available = True
    missing_parts = []

    for part_name in needed_parts:
        part_row = df[df["part_name"] == part_name]
        if not part_row.empty:
            stock = part_row.iloc[0]["stock_qty"]
            reserved = part_row.iloc[0]["reserved_qty"]
            cost = part_row.iloc[0]["unit_price"]
            if stock - reserved > 0:
                parts_to_reserve.append(part_name)
                total_cost += cost
            else:
                available = False
                missing_parts.append(part_name)
        else:
            available = False
            missing_parts.append(part_name)

    if available:
        for part_name in parts_to_reserve:
            df.loc[df["part_name"] == part_name, "reserved_qty"] += 1
            # Update status if low
            curr_stock = df.loc[df["part_name"] == part_name, "stock_qty"].values[0]
            curr_res = df.loc[df["part_name"] == part_name, "reserved_qty"].values[0]
            reorder = df.loc[df["part_name"] == part_name, "reorder_level"].values[0]
            if curr_stock - curr_res <= reorder:
                df.loc[df["part_name"] == part_name, "status"] = "Low Stock"
        df.to_csv(INVENTORY_FILE, index=False)
        return True, ", ".join(parts_to_reserve), float(total_cost), "Parts reserved successfully."
    else:
        return False, "", 0.0, f"Stock unavailable for: {', '.join(missing_parts)}."

def release_parts(parts_string):
    df = get_inventory()
    if df.empty or not parts_string:
        return
    parts = [p.strip() for p in str(parts_string).split(",") if p.strip()]
    for part_name in parts:
        part_row = df[df["part_name"] == part_name]
        if not part_row.empty:
            cur_stock = df.loc[df["part_name"] == part_name, "stock_qty"].item()
            cur_rsv   = df.loc[df["part_name"] == part_name, "reserved_qty"].item()
            df.loc[df["part_name"] == part_name, "stock_qty"]    = max(0, int(cur_stock) - 1)
            df.loc[df["part_name"] == part_name, "reserved_qty"] = max(0, int(cur_rsv)   - 1)
    df.to_csv(INVENTORY_FILE, index=False)

def reorder_part(part_id, qty=10):
    df = get_inventory()
    if df.empty:
        return False
    if part_id in df["spare_part_id"].values:
        df.loc[df["spare_part_id"] == part_id, "stock_qty"] += qty
        df.loc[df["spare_part_id"] == part_id, "status"] = "Available"
        df.to_csv(INVENTORY_FILE, index=False)
        return True
    return False
