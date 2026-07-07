import { useEffect, useState } from "react";

import api from "../api/axios";

const currency = (n) =>
  "₹" + Number(n || 0).toLocaleString("en-IN", { minimumFractionDigits: 2 });

export default function Transactions() {
  const [transactions, setTransactions] = useState([]);
  const [typeFilter, setTypeFilter] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const load = () => {
    setLoading(true);
    const params = typeFilter ? { type: typeFilter } : {};
    api
      .get("/transactions", { params })
      .then((res) => setTransactions(res.data.transactions))
      .catch(() => setError("Failed to load transactions"))
      .finally(() => setLoading(false));
  };

  useEffect(load, [typeFilter]);

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this transaction?")) return;
    try {
      await api.delete(`/transactions/${id}`);
      setTransactions((prev) => prev.filter((t) => t.id !== id));
    } catch {
      setError("Failed to delete transaction");
    }
  };

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h3 className="mb-0">Transactions</h3>
        <select
          className="form-select w-auto"
          value={typeFilter}
          onChange={(e) => setTypeFilter(e.target.value)}
        >
          <option value="">All</option>
          <option value="income">Income</option>
          <option value="expense">Expense</option>
        </select>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      <div className="card shadow-sm">
        <div className="card-body table-wrapper">
          {loading ? (
            <div className="text-center py-4">
              <div className="spinner-border text-brand" role="status" />
            </div>
          ) : (
            <table className="table align-middle mb-0">
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Type</th>
                  <th>Category</th>
                  <th>Description</th>
                  <th>Source</th>
                  <th className="text-end">Amount</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {transactions.length ? (
                  transactions.map((t) => (
                    <tr key={t.id}>
                      <td>{t.transaction_date}</td>
                      <td>
                        <span
                          className={`badge ${
                            t.type === "income" ? "bg-success" : "bg-danger"
                          }`}
                        >
                          {t.type}
                        </span>
                      </td>
                      <td>{t.category}</td>
                      <td>{t.description}</td>
                      <td>
                        <span className="badge bg-secondary">{t.source}</span>
                      </td>
                      <td
                        className={`text-end ${
                          t.type === "income" ? "text-success" : "text-danger"
                        }`}
                      >
                        {t.type === "income" ? "+" : "-"}
                        {currency(t.amount)}
                      </td>
                      <td className="text-end">
                        <button
                          className="btn btn-sm btn-outline-danger"
                          onClick={() => handleDelete(t.id)}
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="7" className="text-center text-muted">
                      No transactions found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
}
