import { useState } from "react";
import { useNavigate } from "react-router-dom";

import api from "../api/axios";

const CATEGORIES = [
  "Food", "Travel", "Bills", "Shopping",
  "Health", "Education", "Entertainment", "Other",
];

const today = new Date().toISOString().slice(0, 10);

export default function UploadReceipt() {
  const navigate = useNavigate();

  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [rawText, setRawText] = useState("");

  // Editable extracted fields (populated after OCR).
  const [extracted, setExtracted] = useState(null);

  const handleFileChange = (e) => {
    const f = e.target.files[0];
    setFile(f);
    setExtracted(null);
    setError("");
    setPreview(f ? URL.createObjectURL(f) : null);
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!file) return;
    setError("");
    setUploading(true);
    try {
      const formData = new FormData();
      formData.append("file", file);
      const res = await api.post("/receipts/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      const r = res.data.receipt;
      setRawText(r.extracted_text || "");
      setExtracted({
        vendor: r.extracted_vendor || "",
        date: r.extracted_date || today,
        amount: r.extracted_amount || "",
        category: r.suggested_category || "Other",
        description: r.extracted_vendor || "Receipt expense",
      });
    } catch (err) {
      setError(
        err.response?.data?.error ||
          "OCR failed. Ensure Tesseract is installed correctly."
      );
    } finally {
      setUploading(false);
    }
  };

  const handleFieldChange = (e) =>
    setExtracted({ ...extracted, [e.target.name]: e.target.value });

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    setError("");
    try {
      await api.post("/receipts/save-as-expense", {
        amount: extracted.amount,
        category: extracted.category,
        description: extracted.description || extracted.vendor,
        vendor: extracted.vendor,
        transaction_date: extracted.date,
      });
      navigate("/transactions");
    } catch (err) {
      setError(err.response?.data?.error || "Failed to save expense");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div>
      <h3 className="mb-4">Upload Receipt</h3>
      {error && <div className="alert alert-danger">{error}</div>}

      <div className="row g-4">
        <div className="col-md-5">
          <div className="card shadow-sm">
            <div className="card-body">
              <form onSubmit={handleUpload}>
                <div className="mb-3">
                  <label className="form-label">Receipt image (png, jpg, jpeg)</label>
                  <input
                    type="file"
                    accept=".png,.jpg,.jpeg"
                    className="form-control"
                    onChange={handleFileChange}
                    required
                  />
                </div>
                {preview && (
                  <img
                    src={preview}
                    alt="Receipt preview"
                    className="img-fluid rounded mb-3 border"
                  />
                )}
                <button className="btn btn-brand w-100" disabled={uploading || !file}>
                  {uploading ? "Scanning..." : "Scan Receipt"}
                </button>
              </form>
            </div>
          </div>
        </div>

        <div className="col-md-7">
          {extracted ? (
            <div className="card shadow-sm">
              <div className="card-body">
                <h5 className="mb-3">Extracted Data (editable)</h5>
                <form onSubmit={handleSave}>
                  <div className="mb-3">
                    <label className="form-label">Vendor</label>
                    <input
                      type="text"
                      name="vendor"
                      className="form-control"
                      value={extracted.vendor}
                      onChange={handleFieldChange}
                    />
                  </div>
                  <div className="row">
                    <div className="col-md-6 mb-3">
                      <label className="form-label">Date</label>
                      <input
                        type="date"
                        name="date"
                        className="form-control"
                        value={extracted.date}
                        onChange={handleFieldChange}
                      />
                    </div>
                    <div className="col-md-6 mb-3">
                      <label className="form-label">Amount</label>
                      <input
                        type="number"
                        step="0.01"
                        name="amount"
                        className="form-control"
                        value={extracted.amount}
                        onChange={handleFieldChange}
                        required
                      />
                    </div>
                  </div>
                  <div className="mb-3">
                    <label className="form-label">Category</label>
                    <select
                      name="category"
                      className="form-select"
                      value={extracted.category}
                      onChange={handleFieldChange}
                    >
                      {CATEGORIES.map((c) => (
                        <option key={c} value={c}>
                          {c}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className="mb-3">
                    <label className="form-label">Description</label>
                    <input
                      type="text"
                      name="description"
                      className="form-control"
                      value={extracted.description}
                      onChange={handleFieldChange}
                    />
                  </div>
                  <button className="btn btn-success w-100" disabled={saving}>
                    {saving ? "Saving..." : "Save as Expense"}
                  </button>
                </form>

                {rawText && (
                  <details className="mt-3">
                    <summary className="text-muted small">View raw OCR text</summary>
                    <pre className="small bg-light p-2 mt-2 rounded">{rawText}</pre>
                  </details>
                )}
              </div>
            </div>
          ) : (
            <div className="card shadow-sm">
              <div className="card-body text-muted">
                Upload and scan a receipt to see extracted vendor, date, amount
                and category here. You can edit everything before saving.
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
