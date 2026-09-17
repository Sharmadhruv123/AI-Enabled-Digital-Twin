import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend
} from "recharts";

export default function HealthChart({ data }) {
  return (
    <div style={{ 
      width: "100%", 
      height: 350, 
      background: "rgba(0,0,0,0.3)", 
      padding: "20px", 
      borderRadius: "15px",
      marginTop: "20px"
    }}>
      <ResponsiveContainer>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
          <XAxis 
            dataKey="time" 
            stroke="#888" 
            fontSize={12}
            tick={{fill: '#888'}}
          />
          <YAxis 
            stroke="#888" 
            fontSize={12}
            tick={{fill: '#888'}}
            domain={[0, 120]}
          />
          <Tooltip 
            contentStyle={{ background: '#111', border: '1px solid #444', borderRadius: '8px' }}
            itemStyle={{ fontSize: '12px' }}
          />
          <Legend wrapperStyle={{ paddingTop: "10px" }} />
          
          <Line 
            name="Temperature (°C)"
            type="monotone" 
            dataKey="temp" 
            stroke="#00f2fe" 
            strokeWidth={3}
            dot={false}
            activeDot={{ r: 6 }}
          />
          
          <Line 
            name="Vibration (Scaled)"
            type="monotone" 
            dataKey="vib" 
            stroke="#f093fb" 
            strokeWidth={3}
            dot={false}
          />

          <Line 
            name="Risk Score (%)"
            type="monotone" 
            dataKey="risk" 
            stroke="#ff003c" 
            strokeWidth={4}
            dot={true}
            strokeDasharray="5 5"
          />
        </LineChart>
      </ResponsiveContainer>
      <div style={{ textAlign: "center", fontSize: "12px", color: "#666", marginTop: "10px" }}>
        * Vibration is scaled (x30) for visualization on the same axis.
      </div>
    </div>
  );
}