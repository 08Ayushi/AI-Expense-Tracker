import { useEffect, useState } from "react";
import { Bar, Line, Pie } from "react-chartjs-2";
import {
  ArcElement,
  BarElement,
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  Tooltip,
} from "chart.js";

import api from "../api/axios";
import ChartCard from "../components/ChartCard.jsx";

ChartJS.register(
  ArcElement,
  BarElement,
  CategoryScale,
  LinearScale,
  LineElement,
  PointElement,
  Tooltip,
  Legend
);

const CHART_COLORS = [
  "#4f46e5", "#22c55e", "#f59e0b", "#ef4444",
  "#06b6d4", "#a855f7", "#ec4899", "#64748b",
];

const currency = (n) =>
  "₹" + Number(n || 0).toLocaleString("en-IN", { minimumFractionDigits: 2 });

export default function Reports() {
  const [monthly, setMonthly] = useState([]);
  const [category, setCategory] = useState([]);
  const [ive, setIve] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([
      api.get("/reports/monthly"),
      api.get("/reports/category"),
      api.get("/reports/income-vs-expense"),
      api.get("/reports/prediction"),
    ])
      .then(([m, c, i, p]) => {
        setMonthly(m.data.monthly);
        setCategory(c.data.category);
        setIve(i.data);
        setPrediction(p.data);
      })
      .catch(() => setError("Failed to load reports"));
  }, []);

  const handleExport = async () => {
    try {
      const res = await api.get("/reports/export-csv", { responseType: "blob" });
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "transactions.csv");
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch {
      setError("Failed to export CSV");
    }
  };

  if (error) return <div className="alert alert-danger">{error}</div>;

  const monthlyData = {
    labels: monthly.map((m) => m.month),
    datasets: [
      {
        label: "Income",
        data: monthly.map((m) => m.income),
        backgroundColor: "#22c55e",
      },
      {
        label: "Expense",
        data: monthly.map((m) => m.expense),
        backgroundColor: "#ef4444",
      },
    ],
  };

  const categoryData = {
    labels: category.map((c) => c.category),
    datasets: [
      {
        data: category.map((c) => c.amount),
        backgroundColor: CHART_COLORS,
      },
    ],
  };

  const iveData = ive && {
    labels: ["Income", "Expense", "Balance"],
    datasets: [
      {
        label: "Amount",
        data: [ive.total_income, ive.total_expense, ive.balance],
        backgroundColor: ["#22c55e", "#ef4444", "#4f46e5"],
      },
    ],
  };

  // Build the prediction line chart from history + predicted point.
  let predictionChart = null;
  if (prediction?.status === "ok") {
    const labels = [
      ...prediction.history.map((h) => h.month),
      prediction.predicted_month,
    ];
    predictionChart = {
      labels,
      datasets: [
        {
          label: "Actual Expense",
          data: [...prediction.history.map((h) => h.expense), null],
          borderColor: "#4f46e5",
          backgroundColor: "#4f46e5",
          tension: 0.3,
        },
        {
          label: "Predicted",
          data: [
            ...prediction.history.map(() => null),
            prediction.predicted_expense,
          ],
          borderColor: "#f59e0b",
          backgroundColor: "#f59e0b",
          borderDash: [6, 6],
          pointRadius: 6,
        },
      ],
    };
  }

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h3 className="mb-0">Reports</h3>
        <button className="btn btn-brand" onClick={handleExport}>
          Export CSV
        </button>
      </div>

      <div className="row g-3 mb-3">
        <div className="col-lg-7">
          <ChartCard title="Monthly Income vs Expense">
            {monthly.length ? (
              <Bar data={monthlyData} options={{ maintainAspectRatio: false }} />
            ) : (
              <p className="text-muted">No data yet.</p>
            )}
          </ChartCard>
        </div>
        <div className="col-lg-5">
          <ChartCard title="Expense by Category">
            {category.length ? (
              <Pie
                data={categoryData}
                options={{ maintainAspectRatio: false, plugins: { legend: { position: "bottom" } } }}
              />
            ) : (
              <p className="text-muted">No expenses yet.</p>
            )}
          </ChartCard>
        </div>
      </div>

      <div className="row g-3">
        <div className="col-lg-5">
          <ChartCard title="Overall Income vs Expense">
            {iveData ? (
              <Bar data={iveData} options={{ maintainAspectRatio: false, plugins: { legend: { display: false } } }} />
            ) : (
              <p className="text-muted">No data yet.</p>
            )}
          </ChartCard>
        </div>
        <div className="col-lg-7">
          <ChartCard title="Next Month Expense Prediction">
            {prediction?.status === "ok" ? (
              <>
                <div className="alert alert-info py-2">
                  Predicted for <strong>{prediction.predicted_month}</strong>:{" "}
                  <strong>{currency(prediction.predicted_expense)}</strong>
                </div>
                <div style={{ height: 220 }}>
                  <Line data={predictionChart} options={{ maintainAspectRatio: false }} />
                </div>
              </>
            ) : (
              <p className="text-muted">
                {prediction?.message || "Not enough data for prediction"}
              </p>
            )}
          </ChartCard>
        </div>
      </div>
    </div>
  );
}
