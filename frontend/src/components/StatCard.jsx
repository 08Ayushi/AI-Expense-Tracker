// Small dashboard summary card showing a labelled value.
export default function StatCard({ title, value, icon, color = "primary" }) {
  return (
    <div className="card stat-card h-100">
      <div className="card-body d-flex align-items-center gap-3">
        <div className={`stat-icon bg-${color} bg-opacity-10 text-${color}`}>
          {icon}
        </div>
        <div>
          <div className="text-muted small">{title}</div>
          <div className="stat-value">{value}</div>
        </div>
      </div>
    </div>
  );
}
