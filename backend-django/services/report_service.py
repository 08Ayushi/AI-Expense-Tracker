"""Reporting service backed by Pandas."""
import io

import pandas as pd

from expenses.models import Transaction


def _transactions_dataframe(user):
    rows = Transaction.objects.filter(user=user)
    records = [t.to_dict() for t in rows]
    df = pd.DataFrame(records)
    if not df.empty:
        df["transaction_date"] = pd.to_datetime(df["transaction_date"])
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0.0)
    return df


def monthly_report(user):
    df = _transactions_dataframe(user)
    if df.empty:
        return []
    df["month"] = df["transaction_date"].dt.strftime("%Y-%m")
    grouped = df.groupby(["month", "type"])["amount"].sum().unstack(fill_value=0).reset_index()
    result = []
    for _, row in grouped.iterrows():
        income = float(row.get("income", 0.0))
        expense = float(row.get("expense", 0.0))
        result.append({
            "month": row["month"],
            "income": round(income, 2),
            "expense": round(expense, 2),
            "balance": round(income - expense, 2),
        })
    return sorted(result, key=lambda r: r["month"])


def category_report(user):
    df = _transactions_dataframe(user)
    if df.empty:
        return []
    expenses = df[df["type"] == "expense"]
    if expenses.empty:
        return []
    grouped = expenses.groupby("category")["amount"].sum().reset_index()
    grouped = grouped.sort_values("amount", ascending=False)
    return [
        {"category": row["category"], "amount": round(float(row["amount"]), 2)}
        for _, row in grouped.iterrows()
    ]


def income_vs_expense(user):
    df = _transactions_dataframe(user)
    if df.empty:
        return {"total_income": 0.0, "total_expense": 0.0, "balance": 0.0}
    total_income = float(df[df["type"] == "income"]["amount"].sum())
    total_expense = float(df[df["type"] == "expense"]["amount"].sum())
    return {
        "total_income": round(total_income, 2),
        "total_expense": round(total_expense, 2),
        "balance": round(total_income - total_expense, 2),
    }


def export_csv(user):
    df = _transactions_dataframe(user)
    if df.empty:
        df = pd.DataFrame(columns=[
            "id", "type", "category", "description",
            "amount", "transaction_date", "source", "created_at",
        ])
    else:
        df = df[[
            "id", "type", "category", "description",
            "amount", "transaction_date", "source", "created_at",
        ]]
        df["transaction_date"] = df["transaction_date"].dt.strftime("%Y-%m-%d")
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue()
