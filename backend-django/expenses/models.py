"""Expense-related models."""
from django.conf import settings
from django.db import models


class Transaction(models.Model):
    TYPE_INCOME = "income"
    TYPE_EXPENSE = "expense"
    TYPE_CHOICES = [(TYPE_INCOME, "Income"), (TYPE_EXPENSE, "Expense")]

    SOURCE_MANUAL = "manual"
    SOURCE_RECEIPT = "receipt"
    SOURCE_CHOICES = [(SOURCE_MANUAL, "Manual"), (SOURCE_RECEIPT, "Receipt")]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions"
    )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.CharField(max_length=80, default="Other")
    description = models.CharField(max_length=255, blank=True, default="")
    amount = models.FloatField()
    transaction_date = models.DateField()
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, default=SOURCE_MANUAL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-transaction_date", "-id"]

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "type": self.type,
            "category": self.category,
            "description": self.description,
            "amount": self.amount,
            "transaction_date": self.transaction_date.isoformat(),
            "source": self.source,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Receipt(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receipts"
    )
    filename = models.CharField(max_length=255)
    extracted_text = models.TextField(blank=True, default="")
    extracted_amount = models.FloatField(null=True, blank=True)
    extracted_date = models.CharField(max_length=40, null=True, blank=True)
    extracted_vendor = models.CharField(max_length=160, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "filename": self.filename,
            "extracted_text": self.extracted_text,
            "extracted_amount": self.extracted_amount,
            "extracted_date": self.extracted_date,
            "extracted_vendor": self.extracted_vendor,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Budget(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="budgets"
    )
    category = models.CharField(max_length=80)
    monthly_limit = models.FloatField()
    month = models.IntegerField()  # 1-12
    year = models.IntegerField()

    class Meta:
        unique_together = ("user", "category", "month", "year")
        ordering = ["-year", "-month"]

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "category": self.category,
            "monthly_limit": self.monthly_limit,
            "month": self.month,
            "year": self.year,
        }
