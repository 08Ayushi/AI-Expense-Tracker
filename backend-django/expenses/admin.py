from django.contrib import admin

from expenses.models import Budget, Receipt, Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "type", "category", "amount", "transaction_date", "source")
    list_filter = ("type", "category", "source")
    search_fields = ("description", "category", "user__email")


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "filename", "extracted_vendor", "extracted_amount", "created_at")
    search_fields = ("filename", "extracted_vendor", "user__email")


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "category", "monthly_limit", "month", "year")
    list_filter = ("month", "year", "category")
