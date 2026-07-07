import { useEffect, useState } from "react";

import api from "../api/axios";

const CATEGORIES = [
  "Food", "Travel", "Bills", "Shopping",
  "Health", "Education", "Entertainment", "Other",
];

const MONTHS = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December",
];

const now = new Date();
const currency = (n) =>
  "₹" + Number(n || 0).toLocaleString("en-IN", { minimumFractionDigits: 2 });

export default function Budgets() {
  const [budgets, setBudgets] = useState([]);
  const [form, setForm] = useState({
    category: "Food",
    monthly_limit: "",
    month: now.getMonth() + 1,
    year: now.getFullYear(),
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const load = () => {
    api
      .get("/budgets")
      .then((res) => setBudgets(res.data.budgets))
      .catch(() => setError("Failed to load budgets"));
  };

  useEffect(load, []);

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    try {
      await api.post("/budgets", form);
      setSuccess("Budget saved!");
      setForm({ ...form, monthly_limit: "" });
      load();
    } catch (err) {
      setError(err.response?.data?.error || "Failed to save budget");
    }
  };

  return (
    <div>
      <h3 className="mb-4">Budgets</h3>
      <div className="row g-4">
        <div className="col-md-5">
          <div className="card shadow-sm">
            <div className="card-body">
              <h5 className="mb-3">Set Monthly Budget</h5>
              {error && <div className="alert alert-danger">{error}</div>}
              {success && <div className="alert alert-success">{success}</div>}
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label className="form-label">Category</label>
                  <select
                    name="category"
                    className="form-select"
                    value={form.category}
                    onChange={handleChange}
                  >
                    {CATEGORIES.map((c) => (
                      <option key={c} value={c}>
                        {c}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="mb-3">
                  <label className="form-label">Monthly Limit</label>
                  <input
                    type="number"
                    step="0.01"
                    min="0"
                    name="monthly_limit"
                    className="form-control"
                    value={form.monthly_limit}
                    onChange={handleChange}
                    required
                  />
                </div>
                <div className="row">
                  <div className="col-6 mb-3">
                    <label className="form-label">Month</label>
                    <select
                      name="month"
                      className="form-select"
                      value={form.month}
                      onChange={handleChange}
                    >
                      {MONTHS.map((m, i) => (
                        <option key={m} value={i + 1}>
                          {m}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="col-6 mb-3">
                    <label className="form-label">Year</label>
                    <input
                      type="number"
                      name="year"
                      className="form-control"
                      value={form.year}
                      onChange={handleChange}
                    />
                  </div>
                </div>
                <button className="btn btn-brand w-100">Save Budget</button>
              </form>
            </div>
          </div>
        </div>

        <div className="col-md-7">
          <div className="card shadow-sm">
            <div className="card-body table-wrapper">
              <h5 className="mb-3">Your Budgets</h5>
              <table className="table align-middle mb-0">
                <thead>
                  <tr>
                    <th>Category</th>
                    <th>Period</th>
                    <th className="text-end">Limit</th>
                  </tr>
                </thead>
                <tbody>
                  {budgets.length ? (
                    budgets.map((b) => (
                      <tr key={b.id}>
                        <td>{b.category}</td>
                        <td>
                          {MONTHS[b.month - 1]} {b.year}
                        </td>
                        <td className="text-end">{currency(b.monthly_limit)}</td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan="3" className="text-center text-muted">
                        No budgets set yet.
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
  );
}
