"""Shared validation helpers."""
import re
from datetime import datetime

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(email):
    return bool(email and EMAIL_RE.match(email.strip()))


def is_non_empty_string(value, min_length=1):
    return isinstance(value, str) and len(value.strip()) >= min_length


def parse_amount(value):
    try:
        amount = float(value)
    except (TypeError, ValueError):
        raise ValueError("Amount must be a number")
    if amount <= 0:
        raise ValueError("Amount must be greater than zero")
    return round(amount, 2)


def parse_date(value, default_today=True):
    if not value:
        if default_today:
            return datetime.utcnow().date()
        raise ValueError("Date is required")
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(str(value).strip(), fmt).date()
        except ValueError:
            continue
    raise ValueError("Invalid date format, expected YYYY-MM-DD")


def validate_transaction_type(value):
    if value not in ("income", "expense"):
        raise ValueError("type must be 'income' or 'expense'")
    return value
