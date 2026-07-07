import os
import uuid

from django.conf import settings
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from expenses.models import Receipt
from services.category_service import detect_category
from services.ocr_service import process_receipt
from services.transaction_service import create_transaction


def _allowed_file(filename):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in settings.ALLOWED_RECEIPT_EXTENSIONS


class ReceiptUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"error": "No file selected"}, status=status.HTTP_400_BAD_REQUEST)
        if not _allowed_file(file.name):
            return Response(
                {"error": "Only png, jpg and jpeg files are allowed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
        unique_name = f"{uuid.uuid4().hex}_{file.name}"
        file_path = os.path.join(settings.MEDIA_ROOT, unique_name)

        with open(file_path, "wb+") as dest:
            for chunk in file.chunks():
                dest.write(chunk)

        try:
            parsed = process_receipt(file_path)
        except Exception as exc:  # noqa: BLE001
            return Response(
                {"error": "OCR failed. Make sure Tesseract is installed.", "details": str(exc)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        category = detect_category(
            f"{parsed.get('extracted_vendor') or ''} {parsed.get('extracted_text') or ''}"
        )

        receipt = Receipt.objects.create(
            user=request.user,
            filename=unique_name,
            extracted_text=parsed.get("extracted_text", ""),
            extracted_amount=parsed.get("extracted_amount"),
            extracted_date=parsed.get("extracted_date"),
            extracted_vendor=parsed.get("extracted_vendor"),
        )

        response = receipt.to_dict()
        response["suggested_category"] = category
        return Response(
            {"message": "Receipt processed", "receipt": response},
            status=status.HTTP_201_CREATED,
        )


class ReceiptSaveAsExpenseView(APIView):
    def post(self, request):
        data = request.data
        payload = {
            "type": "expense",
            "amount": data.get("amount") or data.get("extracted_amount"),
            "category": data.get("category"),
            "description": (
                data.get("description")
                or data.get("vendor")
                or data.get("extracted_vendor")
                or "Receipt expense"
            ),
            "transaction_date": (
                data.get("transaction_date") or data.get("date") or data.get("extracted_date")
            ),
            "source": "receipt",
        }
        transaction, error = create_transaction(request.user, payload)
        if error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)
        return Response(
            {"message": "Expense saved from receipt", "transaction": transaction.to_dict()},
            status=status.HTTP_201_CREATED,
        )
