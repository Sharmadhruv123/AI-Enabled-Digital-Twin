# AI-Enabled Digital Twin | Port Crane Framework

An advanced, interactive Digital Twin framework designed for real-time fleet monitoring, predictive maintenance, and enterprise resource planning (ERP) integration for port crane systems. This application simulates real-time sensor telemetry and leverages AI to predict failures, estimate Remaining Useful Life (RUL), and autonomously manage maintenance workflows.

## 🚀 Key Features

*   **⬡ 2D Structural Digital Twin:** Real-time visual overlay of crane subsystems, updating dynamically based on simulated sensor readings (Vibration, Temperature, Motor Current, Hydraulic Pressure).
*   **◈ AI Predictive Analytics Engine:** Multi-output Machine Learning predictions including Health Score, Remaining Useful Life (RUL), Failure Probability, and Anomaly Detection.
*   **▤ CMMS (Computerized Maintenance Management System):** End-to-end work order lifecycle tracking. Auto-triggers work orders when critical thresholds are breached.
*   **⬢ ERP Spare Parts Inventory:** Automated inventory management that auto-reserves, deducts, and suggests reordering of spare parts based on AI fault diagnostics.
*   **↻ Closed-Loop Feedback:** Technician feedback loop that feeds maintenance data back into the system to retrain and improve AI models continuously.
*   **▧ Reporting & Data Export:** Generate comprehensive HTML/PDF summary reports and download raw datasets (telemetry, work orders, inventory, retraining logs) as CSV files.
*   **⊙ Role-Based Access Control:** Simulates multiple user personas (Administrator, Maintenance Engineer, Reliability Engineer, Port Operations Planner) with tailored permissions.

## 🛠️ Technology Stack

*   **Frontend / UI:** Streamlit (with highly customized CSS/JS for a modern, dark-mode cyber aesthetic)
*   **Data Visualization:** Plotly
*   **Backend Logic:** Python (Pandas, Scikit-learn for ML pipelines)
*   **Data Storage:** CSV-based persistence for lightweight deployment

## ⚙️ How to Run Locally

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Sharmadhruv123/AI-Enabled-Digital-Twin.git
    cd AI-Enabled-Digital-Twin
    ```

2.  **Install dependencies:**
    Make sure you have Python 3.8+ installed.
    ```bash
    pip install streamlit pandas numpy plotly scikit-learn
    ```

3.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

4.  **Access the Dashboard:**
    Open your browser and navigate to `http://localhost:8501`.

## 📁 Project Structure

*   `app.py`: The main Streamlit dashboard application.
*   `prediction_pipeline.py`: AI model logic for evaluating sensor telemetry.
*   `model_retraining.py`: Handles the closed-loop retraining of the AI models.
*   `cmms_service.py`: Logic for Work Order creation and management.
*   `erp_service.py`: Logic for Spare Parts inventory management.
*   `feedback_service.py`: Handles logging of technician feedback.
*   `reporting_service.py`: Generates HTML/PDF summary reports.
*   `auth_service.py`: Role-based access control management.
*   `*.csv`: Data files serving as the database (e.g., `cranes.csv`, `sensor_data.csv`, `work_orders.csv`, `spare_parts.csv`).

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.
