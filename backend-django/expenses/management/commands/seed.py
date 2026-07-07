"""Seed demo data: python manage.py seed"""
from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.core.management.base import BaseCommand

from accounts.models import User
from expenses.models import Budget, Transaction

DEMO_EMAIL = "demo@example.com"
DEMO_PASSWORD = "demo123"


def month_offset(months_ago):
    return datetime.utcnow().date().replace(day=15) - relativedelta(months=months_ago)


class Command(BaseCommand):
    help = "Seed demo user, transactions, and budgets"

    def handle(self, *args, **options):
        User.objects.filter(email=DEMO_EMAIL).delete()

        user = User.objects.create_user(
            email=DEMO_EMAIL,
            name="Demo User",
            password=DEMO_PASSWORD,
        )

        incomes = []
        for m in range(3, -1, -1):
            incomes.append(Transaction(
                user=user, type="income", category="Income",
                description="Monthly Salary", amount=50000,
                transaction_date=month_offset(m), source="manual",
            ))
        incomes.append(Transaction(
            user=user, type="income", category="Income",
            description="Freelance project", amount=12000,
            transaction_date=month_offset(1), source="manual",
        ))

        sample_expenses = [
            ("Food", "Zomato dinner", 850),
            ("Food", "Grocery shopping", 3200),
            ("Travel", "Uber rides", 640),
            ("Travel", "Petrol", 2500),
            ("Bills", "Electricity bill", 1800),
            ("Bills", "Mobile recharge", 499),
            ("Shopping", "Amazon order", 2999),
            ("Health", "Pharmacy medicine", 450),
            ("Entertainment", "Netflix subscription", 649),
            ("Education", "Udemy course", 1299),
        ]

        expenses = []
        for m in range(3, -1, -1):
            for category, desc, amount in sample_expenses:
                variation = 1 + (0.05 * (3 - m))
                expenses.append(Transaction(
                    user=user, type="expense", category=category,
                    description=desc, amount=round(amount * variation, 2),
                    transaction_date=month_offset(m), source="manual",
                ))

        Transaction.objects.bulk_create(incomes + expenses)

        now = datetime.utcnow()
        Budget.objects.bulk_create([
            Budget(user=user, category="Food", monthly_limit=5000, month=now.month, year=now.year),
            Budget(user=user, category="Travel", monthly_limit=4000, month=now.month, year=now.year),
            Budget(user=user, category="Shopping", monthly_limit=3000, month=now.month, year=now.year),
            Budget(user=user, category="Bills", monthly_limit=3000, month=now.month, year=now.year),
        ])

        self.stdout.write(self.style.SUCCESS("Seed complete!"))
        self.stdout.write(f"  Demo login -> email: {DEMO_EMAIL}  password: {DEMO_PASSWORD}")
        self.stdout.write(f"  Users: {User.objects.count()}")
        self.stdout.write(f"  Transactions: {Transaction.objects.count()}")
        self.stdout.write(f"  Budgets: {Budget.objects.count()}")
