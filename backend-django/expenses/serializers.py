from rest_framework import serializers

from expenses.models import Budget, Transaction
from services.validators import parse_amount, parse_date, validate_transaction_type


class TransactionSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    transaction_date = serializers.DateField(format="%Y-%m-%d")

    class Meta:
        model = Transaction
        fields = (
            "id", "user_id", "type", "category", "description",
            "amount", "transaction_date", "source", "created_at",
        )
        read_only_fields = ("id", "user_id", "source", "created_at")

    def to_representation(self, instance):
        return instance.to_dict()


class TransactionCreateSerializer(serializers.Serializer):
    type = serializers.CharField()
    category = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    amount = serializers.FloatField()
    transaction_date = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        try:
            validate_transaction_type(attrs.get("type"))
            parse_amount(attrs.get("amount"))
            if attrs.get("transaction_date"):
                parse_date(attrs.get("transaction_date"))
        except ValueError as exc:
            raise serializers.ValidationError(str(exc)) from exc
        return attrs


class BudgetSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)

    class Meta:
        model = Budget
        fields = ("id", "user_id", "category", "monthly_limit", "month", "year")
        read_only_fields = ("id", "user_id")

    def to_representation(self, instance):
        return instance.to_dict()


class BudgetCreateSerializer(serializers.Serializer):
    category = serializers.CharField()
    monthly_limit = serializers.FloatField()
    month = serializers.IntegerField(required=False)
    year = serializers.IntegerField(required=False)

    def validate_monthly_limit(self, value):
        return parse_amount(value)

    def validate_month(self, value):
        if not 1 <= value <= 12:
            raise serializers.ValidationError("Month must be between 1 and 12")
        return value
