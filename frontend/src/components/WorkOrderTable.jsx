export default function WorkOrderTable({ workOrders }) {

  return (
    <div>
      <h2>Work Orders</h2>

      <table border="1">
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