import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

import LiveClock from "./components/LiveClock";
import CraneCard from "./components/CraneCard";
import HealthChart from "./components/HealthChart";

function App() {

  const [health, setHealth] = useState("");
  const [confidence, setConfidence] = useState(0);
  const [estimatedRul, setEstimatedRul] = useState(0);
  const [riskScore, setRiskScore] = useState(0);
  const [recommendation, setRecommendation] = useState("");
  const [issueDescription, setIssueDescription] = useState("");
  
  const [workOrders, setWorkOrders] = useState([]);
  const [cranes, setCranes] = useState([]);
  const [sensor, setSensor] = useState({});
  const [history, setHistory] = useState([]);

  const loadData = async () => {
    try {
      // Call backend prediction for active AI monitoring
      const prediction = await axios.post(
        "http://localhost:5000/api/predict-health"
      );

      const { 
        health, 
        risk_score, 
        maintenance_recommendation,
        issue_description,
        sensorData 
      } = prediction.data;

      setHealth(health);
      setConfidence(prediction.data.confidence);
      setEstimatedRul(prediction.data.estimated_rul);
      setRiskScore(risk_score);
      setRecommendation(maintenance_recommendation);
      setIssueDescription(issue_description || "All systems nominal.");
      setSensor(sensorData || {});

      // Keep last 20 points for chart
      setHistory(prev => {
        const newPoint = {
          time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
          temp: sensorData.temperature,
          vib: sensorData.vibration * 30,
          risk: risk_score,
          health: health
        };
        return [...prev, newPoint].slice(-20);
      });

      // UPDATE CRANE FLEET STATUS
      setCranes(prev => {
        // If fleet is empty, we don't do anything here (it will be loaded by initial fetch)
        if (prev.length === 0) return prev;

        return prev.map(c => {
          // Crane 3 is the AI-monitored one
          if (c.crane_id == 3 || c.crane_id == "3") {
            return { ...c, status: health === "Normal" ? "Running" : health };
          }
          
          // Simulation: Randomly fluctuate other cranes to make stats "live"
          if (Math.random() > 0.85) { // 15% chance to change status
            const states = ["Running", "Warning", "Critical"];
            const newStatus = states[Math.floor(Math.random() * 3)];
            return { ...c, status: newStatus };
          }
          return c;
        });
      });

      const workRes = await axios.get("http://localhost:5000/api/workorders");
      setWorkOrders(workRes.data);

    } catch (err) {
      console.error("API error:", err);
    }
  };

  // Effect to handle initial load and interval
  useEffect(() => {
    // Initial fetch from backend to populate the base fleet
    const fetchBaseFleet = async () => {
      try {
        const res = await axios.get("http://localhost:5000/api/cranes");
        setCranes(res.data);
      } catch (e) { console.error(e); }
    };
    
    fetchBaseFleet();
    loadData();

    const dataInterval = setInterval(loadData, 5000);
    
    // COMMISSION NEW CRANE EFFECT
    const expansionInterval = setInterval(() => {
      setCranes(prev => {
        if (prev.length >= 10) return prev;
        const nextId = prev.length + 1;
        const newCrane = {
          crane_id: nextId,
          crane_name: `Crane ${nextId}`,
          location: "Terminal B",
          status: "Running"
        };
        console.log(`Commissioning ${newCrane.crane_name}...`);
        return [...prev, newCrane];
      });
    }, 20000); 

    return () => {
      clearInterval(dataInterval);
      clearInterval(expansionInterval);
    };
  }, []);

  // KPI calculations
  const totalCranes = cranes.length;
  const healthyCranes = cranes.filter(c => c.status === "Running" || c.status === "Normal").length;
  const warningCranes = cranes.filter(c => c.status === "Warning").length;
  const criticalCranes = cranes.filter(c => c.status === "Critical" || c.status === "High Risk").length;

  return (
    <div className="container"style={{alignContent:"center", textAlign:"center"}}>

      <h1>⚓ Smart Port AI Control Center</h1>

      <LiveClock />

      <div className="live-indicator">● AI Monitoring Active</div>

      {/* KPI CARDS */}
      <div className="kpi-container">

        <div className="kpi">
          <p>Total Cranes</p>
          <h2>{totalCranes}</h2>
        </div>

        <div className="kpi">
          <p>Healthy</p>
          <h2 style={{ color: "#00ffaa" }}>{healthyCranes}</h2>
        </div>

        <div className="kpi">
          <p>Warning</p>
          <h2 style={{ color: "#ffaa00" }}>{warningCranes}</h2>
        </div>

        <div className="kpi">
          <p>Critical</p>
          <h2 style={{ color: "#ff003c" }}>{criticalCranes}</h2>
        </div>

      </div>

      {/* LIVE SENSOR PANEL */}
      <div className="sensor-panel">

        <div className="sensor-box">
          🌡 Temperature
          <h3>{sensor.temperature?.toFixed?.(1) ?? "--"} °C</h3>
        </div>

        <div className="sensor-box">
          📳 Vibration
          <h3>{sensor.vibration?.toFixed?.(2) ?? "--"}</h3>
        </div>

        <div className="sensor-box">
          ⚡ Motor Current
          <h3>{sensor.motor_current?.toFixed?.(1) ?? "--"} A</h3>
        </div>

        <div className="sensor-box">
          🏗 Load
          <h3>{sensor.load_tons?.toFixed?.(1) ?? "--"} t</h3>
        </div>

        <div className="sensor-box">
          ⏱ Runtime
          <h3>{sensor.runtime_hours?.toFixed?.(0) ?? "--"} h</h3>
        </div>

      </div>

      {/* DIGITAL TWIN CRANES */}
      <div className="crane-grid">

        {cranes.map((crane) => (
          <CraneCard
            key={crane.crane_id}
            id={crane.crane_id}
            status={crane.status}
          />
        ))}

      </div>

      {/* ALERT */}
      {health === "Critical" && (
        <div className="alert">
          ⚠ CRITICAL MAINTENANCE REQUIRED
        </div>
      )}

      {/* ADVANCED AI INSIGHTS */}
      <div className="advanced-insights">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
          <h2>🧠 Advanced AI Insights</h2>
          <div style={{ textAlign: 'right', color: '#4facfe', fontSize: '14px', fontWeight: 'bold' }}>
            UNIT: CRANE-003 | LOCATION: TERMINAL B, BERTH 4
          </div>
        </div>
        
        <div className="insights-grid">
          <div className="insight-card">
            <p>Confidence Level</p>
            <h3>{(confidence * 100).toFixed(1)}%</h3>
            <div className="progress-bar">
               <div className="progress-fill" style={{ width: `${confidence * 100}%`, background: "#00ffaa" }}></div>
            </div>
          </div>
          <div className="insight-card">
            <p>Estimated RUL</p>
            <h3 style={{ color: estimatedRul < 500 ? "#ff003c" : "#00ffaa" }}>
              {estimatedRul.toFixed(1)} <span style={{fontSize: "14px"}}>hours</span>
            </h3>
            <small>Remaining Useful Life</small>
          </div>
          <div className="insight-card">
            <p>Risk Level</p>
            <h3 style={{ color: riskScore > 70 ? "#ff003c" : riskScore > 40 ? "#ffaa00" : "#00ffaa" }}>
              {riskScore}%
            </h3>
            <div className="risk-meter">
               <div className="risk-fill" style={{ width: `${riskScore}%`, background: riskScore > 70 ? "#ff003c" : riskScore > 40 ? "#ffaa00" : "#00ffaa" }}></div>
            </div>
          </div>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px", marginTop: "30px" }}>
          {recommendation && (
            <div className="recommendation">
              <strong>AI Recommendation:</strong> {recommendation}
            </div>
          )}
          <div className="recommendation" style={{ borderColor: "#f093fb", background: "rgba(240, 147, 251, 0.1)" }}>
            <strong>Issue Analysis:</strong> {issueDescription}
          </div>
        </div>
      </div>

      {/* AI STATUS */}
      {health && (
        <div
          className={`status-box ${
            health === "Normal"
              ? "normal"
              : health === "Warning"
              ? "warning"
              : "critical"
          }`}
        >
          System State: {health}
        </div>
      )}

      {/* HEALTH CHART */}
      <h2>📈 Predictive Trend Analysis</h2>
      <HealthChart data={history} />

      {/* WORK ORDERS */}
      <h2>🛠 Maintenance Work Orders</h2>

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Crane</th>
            <th>Issue</th>
            <th>Priority</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>

          {workOrders.map((wo) => (
            <tr key={wo.id}>
              <td>{wo.id}</td>
              <td>{wo.crane_id}</td>
              <td>{wo.issue}</td>
              <td>{wo.priority}</td>
              <td>{wo.status}</td>
            </tr>
          ))}

        </tbody>

      </table>

    </div>
  );
}

export default App;