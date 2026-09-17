const express = require("express");
const axios = require("axios");
const router = express.Router();
const { v4: uuidv4 } = require("uuid");

let workOrders = [];
let scenarioCounter = 0;

function generateSensorData() {
  const scenarios = ["normal", "warning", "critical"];
  const currentScenario = scenarios[Math.floor(scenarioCounter / 5) % 3];
  scenarioCounter++;

  let temperature, vibration, load_tons, motor_current, runtime_hours;

  if (currentScenario === "normal") {
    temperature = 60 + Math.random() * 5;
    vibration = 0.3 + Math.random() * 0.2;
    load_tons = 15 + Math.random() * 5;
    motor_current = 30 + Math.random() * 5;
    runtime_hours = 1200;
  } else if (currentScenario === "warning") {
    temperature = 78 + Math.random() * 4; 
    vibration = 0.9 + Math.random() * 0.3;
    load_tons = 22 + Math.random() * 3;
    motor_current = 45 + Math.random() * 5;
    runtime_hours = 2500;
  } else { 
    temperature = 92 + Math.random() * 6;
    vibration = 2.4 + Math.random() * 1.2; 
    load_tons = 24 + Math.random() * 2;
    motor_current = 58 + Math.random() * 8;
    runtime_hours = 3000;
  }

  return {
    temperature,
    vibration,
    load_tons,
    motor_current,
    runtime_hours,
    ambient_temp: 28 + Math.random() * 6,
    temp_rolling_avg: temperature,
    vib_rolling_avg: vibration
  };
}

router.post("/predict-health", async (req, res) => {
  const sensorData = generateSensorData();
  let health_status, confidence, estimated_rul_hours, risk_score, maintenance_recommendation, issue_description;

  try {
    const response = await axios.post(
      "http://127.0.0.1:8000/predict",
      sensorData,
      { timeout: 2000 }
    );
    health_status = response.data.health_status;
    confidence = response.data.confidence;
    estimated_rul_hours = response.data.estimated_rul_hours;
    risk_score = response.data.risk_score;
    maintenance_recommendation = response.data.maintenance_recommendation;
    issue_description = response.data.issue_description;
  } catch (err) {
    // Robust fallback AI prediction calculation
    const temp = sensorData.temperature;
    const vib = sensorData.vibration;

    if (temp > 88 || vib > 2.0) {
      health_status = "Critical";
      confidence = 0.95;
      estimated_rul_hours = Math.floor(20 + Math.random() * 30);
      risk_score = 92;
      maintenance_recommendation = "EMERGENCY: Immediate shutdown and work order creation required. Inspect bearing sets.";
      issue_description = "Critical Gearbox/Motor Strain & Overheating";
    } else if (temp > 75 || vib > 0.8) {
      health_status = "Warning";
      confidence = 0.88;
      estimated_rul_hours = Math.floor(300 + Math.random() * 200);
      risk_score = 55;
      maintenance_recommendation = "Schedule maintenance within 24 hours. Check lubrication and wire rope tension.";
      issue_description = "High Bearing Wear & Elevated Temperature";
    } else {
      health_status = "Normal";
      confidence = 0.98;
      estimated_rul_hours = Math.floor(1000 + Math.random() * 400);
      risk_score = 12;
      maintenance_recommendation = "Equipment operating within optimal parameters. Continue regular monitoring.";
      issue_description = "All Subsystems Nominal";
    }
  }

  let work_order = null;

  if (health_status === "Critical" || risk_score > 80) {
    work_order = {
      id: uuidv4(),
      crane_id: 3,
      issue: issue_description || maintenance_recommendation || "High Risk Detected",
      priority: "Emergency",
      status: "Pending"
    };

    workOrders.push(work_order);
  }

  res.json({
    health: health_status,
    confidence,
    estimated_rul: estimated_rul_hours,
    risk_score,
    maintenance_recommendation,
    issue_description,
    work_order,
    sensorData
  });
});

router.get("/workorders", (req, res) => {
  res.json(workOrders);
});

module.exports = router;