from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from expenses.models import Budget
from expenses.serializers import BudgetCreateSerializer


class BudgetListCreateView(APIView):
    def get(self, request):
        qs = Budget.objects.filter(user=request.user)
        month = request.query_params.get("month")
        year = request.query_params.get("year")
        if month:
            qs = qs.filter(month=int(month))
        if year:
            qs = qs.filter(year=int(year))
        budgets = qs.order_by("-year", "-month")
        return Response({"budgets": [b.to_dict() for b in budgets]})

    def post(self, request):
        serializer = BudgetCreateSerializer(data=request.data)
        if not serializer.is_valid():
            error = next(iter(serializer.errors.values()))[0]
            return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)

        now = datetime.utcnow()
        category = serializer.validated_data["category"].strip()
        monthly_limit = serializer.validated_data["monthly_limit"]
        month = serializer.validated_data.get("month") or now.month
        year = serializer.validated_data.get("year") or now.year

        budget, _ = Budget.objects.update_or_create(
            user=request.user,
            category=category,
            month=month,
            year=year,
            defaults={"monthly_limit": monthly_limit},
        )
        return Response(
            {"message": "Budget saved", "budget": budget.to_dict()},
            status=status.HTTP_201_CREATED,
        )
