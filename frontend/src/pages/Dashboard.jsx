import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Doughnut } from "react-chartjs-2";
import {
  ArcElement,
  Chart as ChartJS,
  Legend,
  Tooltip,
} from "chart.js";

import api from "../api/axios";
import ChartCard from "../components/ChartCard.jsx";
import StatCard from "../components/StatCard.jsx";

ChartJS.register(ArcElement, Tooltip, Legend);

const CHART_COLORS = [
  "#4f46e5", "#22c55e", "#f59e0b", "#ef4444",
  "#06b6d4", "#a855f7", "#ec4899", "#64748b",
];

const currency = (n) =>
  "₹" + Number(n || 0).toLocaleString("en-IN", { minimumFractionDigits: 2 });

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .get("/dashboard")
      .then((res) => setData(res.data))
      .catch(() => setError("Failed to load dashboard"));
  }, []);

  if (error) return <div className="alert alert-danger">{error}</div>;
  if (!data)
    return (
      <div className="text-center py-5">
        <div className="spinner-border text-brand" role="status" />
      </div>
    );

  const categories = data.category_wise_spending || [];
  const doughnutData = {
    labels: categories.map((c) => c.category),
    datasets: [
      {
        data: categories.map((c) => c.amount),
        backgroundColor: CHART_COLORS,
        borderWidth: 1,
      },
    ],
  };

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h3 className="mb-0">Dashboard</h3>
        <div className="d-flex gap-2">
          <Link to="/add" className="btn btn-brand btn-sm">
            + Add Transaction
          </Link>
          <Link to="/upload-receipt" className="btn btn-outline-secondary btn-sm">
            Upload Receipt
          </Link>
        </div>
      </div>

      {/* Budget warnings */}
      {data.budget_warnings?.length > 0 && (
        <div className="alert alert-warning">
          <strong>Budget alerts:</strong>
          <ul className="mb-0">
            {data.budget_warnings.map((w) => (
              <li key={w.category}>
                {w.category}: spent {currency(w.spent)} of {currency(w.limit)} (
                {w.percentage}%)
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Stat cards */}
      <div className="row g-3 mb-4">
        <div className="col-md-3 col-sm-6">
          <StatCard title="Total Income" value={currency(data.total_income)} icon="⬆️" color="success" />
        </div>
        <div className="col-md-3 col-sm-6">
          <StatCard title="Total Expense" value={currency(data.total_expense)} icon="⬇️" color="danger" />
        </div>
        <div className="col-md-3 col-sm-6">
          <StatCard title="Balance" value={currency(data.balance)} icon="💰" color="primary" />
        </div>
        <div className="col-md-3 col-sm-6">
          <StatCard title="This Month" value={currency(data.monthly_spending)} icon="📅" color="warning" />
        </div>
      </div>

      <div className="row g-3">
        <div className="col-lg-5">
          <ChartCard title="Category-wise Spending (This Month)">
            {categories.length ? (
              <Doughnut
                data={doughnutData}
                options={{ maintainAspectRatio: false, plugins: { legend: { position: "bottom" } } }}
              />
            ) : (
              <p className="text-muted">No expenses this month yet.</p>
            )}
          </ChartCard>
        </div>

        <div className="col-lg-7">
          <div className="card chart-card h-100">
            <div className="card-body">
              <h6 className="card-title mb-3">Recent Transactions</h6>
              <div className="table-wrapper">
                <table className="table table-sm align-middle mb-0">
                  <thead>
                    <tr>
                      <th>Date</th>
                      <th>Category</th>
                      <th>Description</th>
                      <th className="text-end">Amount</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.recent_transactions?.length ? (
                      data.recent_transactions.map((t) => (
                        <tr key={t.id}>
                          <td>{t.transaction_date}</td>
                          <td>{t.category}</td>
                          <td>{t.description}</td>
                          <td
                            className={`text-end ${
                              t.type === "income" ? "text-success" : "text-danger"
                            }`}
                          >
                            {t.type === "income" ? "+" : "-"}
                            {currency(t.amount)}
                          </td>
                        </tr>
                      ))
                    ) : (
                      <tr>
                        <td colSpan="4" className="text-muted text-center">
                          No transactions yet.
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
