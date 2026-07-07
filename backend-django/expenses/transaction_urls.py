from django.urls import path

from expenses.transaction_views import TransactionDeleteView, TransactionListCreateView

urlpatterns = [
    path("", TransactionListCreateView.as_view()),
    path("<int:pk>", TransactionDeleteView.as_view()),
]
