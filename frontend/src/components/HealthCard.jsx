import { useState } from "react";
import { API } from "../api";

export default function HealthCard({ setWorkOrder }) {

  const [health, setHealth] = useState("");

  const predictHealth = async () => {

    const res = await API.post("/predict-health", {
      crane_id: 3,
      temperature: 95,
      vibration: 1.4,
      load_tons: 25,
      motor_current: 55,
      runtime_hours: 7000
    });

    setHealth(res.data.health);

    if (res.data.work_order) {
      setWorkOrder(prev => [...prev, res.data.work_order]);
    }
  };

  return (
    <div className="card">
      <h2>Crane Health</h2>

      <button onClick={predictHealth}>Predict</button>

      <h3>{health}</h3>
    </div>
  );
}