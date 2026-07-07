from django.urls import path

from reports.views import (
    CategoryReportView,
    ExportCsvView,
    IncomeVsExpenseView,
    MonthlyReportView,
    PredictionView,
)

urlpatterns = [
    path("monthly", MonthlyReportView.as_view()),
    path("category", CategoryReportView.as_view()),
    path("income-vs-expense", IncomeVsExpenseView.as_view()),
    path("prediction", PredictionView.as_view()),
    path("export-csv", ExportCsvView.as_view()),
]
