import { useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../api/axios";

const CATEGORIES = [
  "Food", "Travel", "Bills", "Shopping",
  "Health", "Education", "Entertainment", "Other",
];

const today = new Date().toISOString().slice(0, 10);

export default function AddTransaction() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    type: "expense",
    category: "Food",
    description: "",
    amount: "",
    transaction_date: today,
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);
    try {
      const payload = { ...form };
      // Income doesn't need a category selection.
      if (payload.type === "income") payload.category = "Income";
      await api.post("/transactions", payload);
      setSuccess("Transaction added successfully!");
      setTimeout(() => navigate("/transactions"), 800);
    } catch (err) {
      setError(err.response?.data?.error || "Failed to add transaction");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card auth-card shadow-sm">
      <div className="card-body p-4">
        <h3 className="mb-4">Add Income / Expense</h3>
        {error && <div className="alert alert-danger">{error}</div>}
        {success && <div className="alert alert-success">{success}</div>}
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Type</label>
            <select
              name="type"
              className="form-select"
              value={form.type}
              onChange={handleChange}
            >
              <option value="expense">Expense</option>
              <option value="income">Income</option>
            </select>
          </div>

          {form.type === "expense" && (
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
          )}

          <div className="mb-3">
            <label className="form-label">Description</label>
            <input
              type="text"
              name="description"
              className="form-control"
              placeholder="e.g. Lunch at cafe"
              value={form.description}
              onChange={handleChange}
            />
          </div>

          <div className="mb-3">
            <label className="form-label">Amount</label>
            <input
              type="number"
              step="0.01"
              min="0"
              name="amount"
              className="form-control"
              value={form.amount}
              onChange={handleChange}
              required
            />
          </div>

          <div className="mb-3">
            <label className="form-label">Date</label>
            <input
              type="date"
              name="transaction_date"
              className="form-control"
              value={form.transaction_date}
              onChange={handleChange}
              required
            />
          </div>

          <button className="btn btn-brand w-100" disabled={loading}>
            {loading ? "Saving..." : "Save Transaction"}
          </button>
        </form>
      </div>
    </div>
  );
}
