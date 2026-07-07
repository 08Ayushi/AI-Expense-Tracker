from django.urls import path

from expenses.receipt_views import ReceiptSaveAsExpenseView, ReceiptUploadView

urlpatterns = [
    path("upload", ReceiptUploadView.as_view()),
    path("save-as-expense", ReceiptSaveAsExpenseView.as_view()),
]
