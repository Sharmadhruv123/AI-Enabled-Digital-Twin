export default function CraneCard({ id, status }) {
  return (
    <div className={`crane-card ${status.toLowerCase()}`}>
      <h3>Crane {id}</h3>
      <p>{status}</p>
    </div>
  );
}