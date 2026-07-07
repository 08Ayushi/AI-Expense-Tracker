// A titled card wrapper for charts (keeps chart sizing consistent).
export default function ChartCard({ title, children, height = 300 }) {
  return (
    <div className="card chart-card h-100">
      <div className="card-body">
        {title && <h6 className="card-title mb-3">{title}</h6>}
        <div style={{ height }}>{children}</div>
      </div>
    </div>
  );
}
