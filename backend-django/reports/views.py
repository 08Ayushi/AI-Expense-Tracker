from datetime import datetime

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from expenses.models import Budget, Transaction
from services.prediction_service import predict_next_month_expense
from services.report_service import (
    category_report,
    export_csv,
    income_vs_expense,
    monthly_report,
)


class DashboardView(APIView):
    def get(self, request):
        user = request.user
        now = datetime.utcnow()
        transactions = Transaction.objects.filter(user=user)

        total_income = sum(t.amount for t in transactions if t.type == "income")
        total_expense = sum(t.amount for t in transactions if t.type == "expense")
        balance = total_income - total_expense

        monthly_spending = sum(
            t.amount
            for t in transactions
            if t.type == "expense"
            and t.transaction_date.month == now.month
            and t.transaction_date.year == now.year
        )

        category_wise = {}
        for t in transactions:
            if (
                t.type == "expense"
                and t.transaction_date.month == now.month
                and t.transaction_date.year == now.year
            ):
                category_wise[t.category] = category_wise.get(t.category, 0) + t.amount

        category_wise_spending = [
            {"category": cat, "amount": round(amt, 2)}
            for cat, amt in sorted(category_wise.items(), key=lambda x: -x[1])
        ]

        recent = transactions.order_by("-transaction_date", "-id")[:5]
        recent_transactions = [t.to_dict() for t in recent]

        budgets = Budget.objects.filter(user=user, month=now.month, year=now.year)
        budget_warnings = []
        for budget in budgets:
            spent = category_wise.get(budget.category, 0)
            if budget.monthly_limit > 0:
                pct = (spent / budget.monthly_limit) * 100
                if pct >= 80:
                    budget_warnings.append({
                        "category": budget.category,
                        "spent": round(spent, 2),
                        "limit": round(budget.monthly_limit, 2),
                        "percentage": round(pct, 1),
                    })

        return Response({
            "total_income": round(total_income, 2),
            "total_expense": round(total_expense, 2),
            "balance": round(balance, 2),
            "monthly_spending": round(monthly_spending, 2),
            "category_wise_spending": category_wise_spending,
            "recent_transactions": recent_transactions,
            "budget_warnings": budget_warnings,
        })


class MonthlyReportView(APIView):
    def get(self, request):
        return Response({"monthly": monthly_report(request.user)})


class CategoryReportView(APIView):
    def get(self, request):
        return Response({"category": category_report(request.user)})


class IncomeVsExpenseView(APIView):
    def get(self, request):
        return Response(income_vs_expense(request.user))


class PredictionView(APIView):
    def get(self, request):
        return Response(predict_next_month_expense(request.user))


class ExportCsvView(APIView):
    def get(self, request):
        csv_data = export_csv(request.user)
        response = HttpResponse(csv_data, content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="transactions.csv"'
        return response
