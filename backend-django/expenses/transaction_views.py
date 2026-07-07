from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from expenses.serializers import TransactionCreateSerializer, TransactionSerializer
from services.transaction_service import create_transaction, delete_transaction, list_transactions


class TransactionListCreateView(APIView):
    def get(self, request):
        t_type = request.query_params.get("type")
        category = request.query_params.get("category")
        transactions = list_transactions(request.user, t_type, category)
        return Response({"transactions": [t.to_dict() for t in transactions]})

    def post(self, request):
        serializer = TransactionCreateSerializer(data=request.data)
        if not serializer.is_valid():
            error = next(iter(serializer.errors.values()))[0]
            return Response({"error": str(error)}, status=status.HTTP_400_BAD_REQUEST)
        transaction, error = create_transaction(request.user, request.data)
        if error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"message": "Transaction created", "transaction": transaction.to_dict()},
            status=status.HTTP_201_CREATED,
        )


class TransactionDeleteView(APIView):
    def delete(self, request, pk):
        ok, error = delete_transaction(request.user, pk)
        if not ok:
            return Response({"error": error}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Transaction deleted"})
