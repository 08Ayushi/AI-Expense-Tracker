"""Next-month expense prediction using scikit-learn Linear Regression."""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

from expenses.models import Transaction


def predict_next_month_expense(user):
    rows = Transaction.objects.filter(user=user, type="expense")
    if not rows.exists():
        return {"status": "insufficient", "message": "Not enough data for prediction"}

    df = pd.DataFrame([t.to_dict() for t in rows])
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
    df["month"] = df["transaction_date"].dt.to_period("M")

    monthly = df.groupby("month")["amount"].sum().sort_index()
    if len(monthly) < 3:
        return {"status": "insufficient", "message": "Not enough data for prediction"}

    x = np.arange(len(monthly)).reshape(-1, 1)
    y = monthly.values.astype(float)
    model = LinearRegression()
    model.fit(x, y)

    predicted = float(model.predict(np.array([[len(monthly)]]))[0])
    predicted = max(predicted, 0.0)
    next_period = monthly.index[-1] + 1

    history = [
        {"month": str(period), "expense": round(float(value), 2)}
        for period, value in monthly.items()
    ]
    return {
        "status": "ok",
        "predicted_month": str(next_period),
        "predicted_expense": round(predicted, 2),
        "history": history,
    }
