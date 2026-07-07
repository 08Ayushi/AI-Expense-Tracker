import { Link } from "react-router-dom";

import { useAuth } from "../context/AuthContext.jsx";

export default function Landing() {
  const { user } = useAuth();

  const features = [
    { icon: "🧾", title: "Receipt OCR", text: "Snap a receipt and let AI extract vendor, date and amount." },
    { icon: "🏷️", title: "Auto Categorization", text: "Expenses are auto-sorted into smart categories." },
    { icon: "📊", title: "Rich Reports", text: "Monthly, category and income vs expense charts." },
    { icon: "🔮", title: "Spend Prediction", text: "ML-powered next-month expense forecasting." },
    { icon: "💰", title: "Budgets", text: "Set monthly limits and get 80% warnings." },
    { icon: "📥", title: "CSV Export", text: "Download all your transactions anytime." },
  ];

  return (
    <div>
      <section className="hero text-center mb-5">
        <h1 className="display-4">Track Expenses with AI</h1>
        <p className="lead mt-3 mb-4">
          Upload receipts, auto-categorize spending, visualise reports and
          predict next month's expenses — all in one place.
        </p>
        <div className="d-flex justify-content-center gap-3">
          {user ? (
            <Link to="/dashboard" className="btn btn-light btn-lg">
              Go to Dashboard
            </Link>
          ) : (
            <>
              <Link to="/register" className="btn btn-light btn-lg">
                Get Started
              </Link>
              <Link to="/login" className="btn btn-outline-light btn-lg">
                Login
              </Link>
            </>
          )}
        </div>
      </section>

      <section>
        <h2 className="text-center mb-4">Features</h2>
        <div className="row g-4">
          {features.map((f) => (
            <div className="col-md-4" key={f.title}>
              <div className="card h-100">
                <div className="card-body">
                  <div className="fs-1">{f.icon}</div>
                  <h5 className="mt-2">{f.title}</h5>
                  <p className="text-muted mb-0">{f.text}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
