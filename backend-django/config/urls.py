from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path

from accounts.views import LoginView, LogoutView, MeView, RegisterView
from expenses.budget_views import BudgetListCreateView
from expenses.receipt_views import ReceiptSaveAsExpenseView, ReceiptUploadView
from expenses.transaction_views import TransactionDeleteView, TransactionListCreateView
from reports.views import (
    CategoryReportView,
    DashboardView,
    ExportCsvView,
    IncomeVsExpenseView,
    MonthlyReportView,
    PredictionView,
)


def health(_request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health", health),
    # Auth
    path("api/auth/register", RegisterView.as_view()),
    path("api/auth/login", LoginView.as_view()),
    path("api/auth/logout", LogoutView.as_view()),
    path("api/auth/me", MeView.as_view()),
    # Transactions
    path("api/transactions", TransactionListCreateView.as_view()),
    path("api/transactions/<int:pk>", TransactionDeleteView.as_view()),
    # Receipts
    path("api/receipts/upload", ReceiptUploadView.as_view()),
    path("api/receipts/save-as-expense", ReceiptSaveAsExpenseView.as_view()),
    # Budgets
    path("api/budgets", BudgetListCreateView.as_view()),
    # Dashboard & reports
    path("api/dashboard", DashboardView.as_view()),
    path("api/reports/monthly", MonthlyReportView.as_view()),
    path("api/reports/category", CategoryReportView.as_view()),
    path("api/reports/income-vs-expense", IncomeVsExpenseView.as_view()),
    path("api/reports/prediction", PredictionView.as_view()),
    path("api/reports/export-csv", ExportCsvView.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
