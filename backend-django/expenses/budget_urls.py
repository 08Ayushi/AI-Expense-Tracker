from django.urls import path

from expenses.budget_views import BudgetListCreateView

urlpatterns = [
    path("", BudgetListCreateView.as_view()),
]
