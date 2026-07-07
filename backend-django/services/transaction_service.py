"""Transaction business logic."""
from expenses.models import Transaction
from services.category_service import detect_category
from services.validators import parse_amount, parse_date, validate_transaction_type


def create_transaction(user, data):
    try:
        t_type = validate_transaction_type(data.get("type"))
        amount = parse_amount(data.get("amount"))
        t_date = parse_date(data.get("transaction_date"))
    except ValueError as exc:
        return None, str(exc)

    description = (data.get("description") or "").strip()
    category = (data.get("category") or "").strip()
    if not category:
        category = detect_category(description) if t_type == "expense" else "Income"

    source = data.get("source") or "manual"
    if source not in ("manual", "receipt"):
        source = "manual"

    transaction = Transaction.objects.create(
        user=user,
        type=t_type,
        category=category,
        description=description,
        amount=amount,
        transaction_date=t_date,
        source=source,
    )
    return transaction, None


def list_transactions(user, t_type=None, category=None):
    qs = Transaction.objects.filter(user=user)
    if t_type in ("income", "expense"):
        qs = qs.filter(type=t_type)
    if category:
        qs = qs.filter(category=category)
    return qs.order_by("-transaction_date", "-id")


def delete_transaction(user, transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id, user=user)
    except Transaction.DoesNotExist:
        return False, "Transaction not found"
    transaction.delete()
    return True, None
