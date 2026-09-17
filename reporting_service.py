import pandas as pd
import os
from datetime import datetime

ROOT_DIR = os.path.dirname(__file__)

def generate_pdf_summary_html(crane_df, wo_df, inv_df, retrain_df):
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Port Crane Digital Twin & Maintenance Summary Report</title>
        <style>
            body {{ font-family: 'Helvetica Neue', Arial, sans-serif; margin: 30px; color: #222; background: #fff; }}
            h1 {{ color: #103b68; border-bottom: 3px solid #103b68; padding-bottom: 10px; }}
            h2 {{ color: #1e5288; margin-top: 25px; font-size: 1.2rem; }}
            .header-info {{ font-size: 0.9rem; color: #666; margin-bottom: 20px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; margin-bottom: 20px; font-size: 0.85rem; }}
            th, td {{ border: 1px solid #ddd; padding: 8px 12px; text-align: left; }}
            th {{ background-color: #f2f5f8; color: #333; font-weight: bold; }}
            tr:nth-child(even) {{ background-color: #fafafa; }}
            .badge-normal {{ background: #d4edda; color: #155724; padding: 3px 8px; border-radius: 4px; font-weight: bold; }}
            .badge-warning {{ background: #fff3cd; color: #856404; padding: 3px 8px; border-radius: 4px; font-weight: bold; }}
            .badge-critical {{ background: #f8d7da; color: #721c24; padding: 3px 8px; border-radius: 4px; font-weight: bold; }}
            .footer {{ margin-top: 40px; font-size: 0.8rem; color: #888; text-align: center; border-top: 1px solid #eee; padding-top: 10px; }}
        </style>
    </head>
    <body>
        <h1>🏗️ Port Crane Digital Twin & Predictive Maintenance Report</h1>
        <div class="header-info">
            <strong>Institution:</strong> CHRIST (Deemed to be University) — MCA Project<br>
            <strong>Author:</strong> Sharma Dhruv Vinodkumar | <strong>Generated On:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}<br>
            <strong>Framework:</strong> AI-Enabled Digital Twin via Closed-Loop CMMS/ERP Integration
        </div>

        <h2>1. Crane Fleet Operational Status</h2>
        <table>
            <thead>
                <tr>
                    <th>Crane ID</th><th>Crane Name</th><th>Type</th><th>Location</th><th>Status</th>
                </tr>
            </thead>
            <tbody>
    """
    for _, row in crane_df.iterrows():
        st = str(row.get('status', 'Running'))
        badge_cls = "badge-normal" if st in ["Running", "Normal"] else ("badge-warning" if st == "Warning" else "badge-critical")
        html_content += f"""
                <tr>
                    <td>{row.get('crane_id','')}</td>
                    <td>{row.get('crane_name','')}</td>
                    <td>{row.get('crane_type','')}</td>
                    <td>{row.get('location','')}</td>
                    <td><span class="{badge_cls}">{st}</span></td>
                </tr>
        """

    html_content += """
            </tbody>
        </table>

        <h2>2. Active CMMS Work Orders</h2>
        <table>
            <thead>
                <tr>
                    <th>WO ID</th><th>Crane ID</th><th>Issue</th><th>Priority</th><th>Action</th><th>Assigned Parts</th><th>Cost ($)</th><th>Status</th>
                </tr>
            </thead>
            <tbody>
    """
    for _, row in wo_df.iterrows():
        html_content += f"""
                <tr>
                    <td>WO-{row.get('work_order_id','')}</td>
                    <td>{row.get('crane_id','')}</td>
                    <td>{row.get('issue','')}</td>
                    <td>{row.get('priority','')}</td>
                    <td>{row.get('action','')}</td>
                    <td>{row.get('assigned_parts','')}</td>
                    <td>${row.get('total_cost', 0):,.2f}</td>
                    <td>{row.get('status','')}</td>
                </tr>
        """

    html_content += """
            </tbody>
        </table>

        <h2>3. ERP Spare Parts Inventory</h2>
        <table>
            <thead>
                <tr>
                    <th>Part ID</th><th>Part Name</th><th>Category</th><th>Stock Qty</th><th>Reserved Qty</th><th>Reorder Level</th><th>Unit Price ($)</th>
                </tr>
            </thead>
            <tbody>
    """
    for _, row in inv_df.iterrows():
        html_content += f"""
                <tr>
                    <td>{row.get('spare_part_id','')}</td>
                    <td>{row.get('part_name','')}</td>
                    <td>{row.get('category','')}</td>
                    <td>{row.get('stock_qty','')}</td>
                    <td>{row.get('reserved_qty','')}</td>
                    <td>{row.get('reorder_level','')}</td>
                    <td>${row.get('unit_price', 0):,.2f}</td>
                </tr>
        """

    html_content += """
            </tbody>
        </table>

        <h2>4. Closed-Loop AI Retraining Log</h2>
        <table>
            <thead>
                <tr>
                    <th>Retrain ID</th><th>Model Name</th><th>Algorithm</th><th>Retrain Date</th><th>Version</th><th>Performance Score</th>
                </tr>
            </thead>
            <tbody>
    """
    for _, row in retrain_df.iterrows():
        html_content += f"""
                <tr>
                    <td>{row.get('retrain_id','')}</td>
                    <td>{row.get('model_name','')}</td>
                    <td>{row.get('algorithm','')}</td>
                    <td>{row.get('retrain_date','')}</td>
                    <td>{row.get('model_version','')}</td>
                    <td>{row.get('performance_score','')}</td>
                </tr>
        """

    html_content += """
            </tbody>
        </table>

        <div class="footer">
            Report generated by AI-Enabled Digital Twin System for Smart Predictive Maintenance of Port Cranes © 2026
        </div>
    </body>
    </html>
    """
    return html_content
