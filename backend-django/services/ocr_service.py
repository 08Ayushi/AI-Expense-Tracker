"""Receipt OCR service (OpenCV + pytesseract)."""
import re
from datetime import datetime

import cv2
import pytesseract
from django.conf import settings

if settings.TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = settings.TESSERACT_CMD


def preprocess_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Could not read the uploaded image")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    denoised = cv2.medianBlur(gray, 3)
    thresh = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 11
    )
    return thresh


def extract_text(image_path):
    processed = preprocess_image(image_path)
    text = pytesseract.image_to_string(processed, config="--psm 6")
    return text or ""


def _parse_amount(text):
    total_keywords = ("grand total", "total", "amount", "balance", "paid")
    candidate = None
    for line in text.splitlines():
        lowered = line.lower()
        if any(k in lowered for k in total_keywords):
            numbers = re.findall(r"\d+[.,]?\d*", line.replace(",", ""))
            for num in numbers:
                try:
                    value = float(num)
                    if candidate is None or value > candidate:
                        candidate = value
                except ValueError:
                    continue
    if candidate is not None:
        return round(candidate, 2)
    all_numbers = re.findall(r"\d+\.\d{2}", text)
    values = [float(n) for n in all_numbers if n]
    if values:
        return round(max(values), 2)
    return None


def _parse_date(text):
    patterns = [
        (r"\b(\d{4}-\d{2}-\d{2})\b", ["%Y-%m-%d"]),
        (r"\b(\d{2}[/-]\d{2}[/-]\d{4})\b", ["%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y"]),
        (r"\b(\d{2}[/-]\d{2}[/-]\d{2})\b", ["%d/%m/%y", "%m/%d/%y", "%d-%m-%y"]),
    ]
    for regex, formats in patterns:
        match = re.search(regex, text)
        if match:
            for fmt in formats:
                try:
                    parsed = datetime.strptime(match.group(1), fmt)
                    return parsed.strftime("%Y-%m-%d")
                except ValueError:
                    continue
            return match.group(1)
    return None


def _parse_vendor(text):
    for line in text.splitlines():
        cleaned = line.strip()
        if len(cleaned) >= 3 and re.search(r"[A-Za-z]", cleaned):
            if sum(c.isalpha() for c in cleaned) >= 3:
                return cleaned[:120]
    return None


def parse_receipt_text(text):
    return {
        "extracted_vendor": _parse_vendor(text),
        "extracted_date": _parse_date(text),
        "extracted_amount": _parse_amount(text),
    }


def process_receipt(image_path):
    text = extract_text(image_path)
    parsed = parse_receipt_text(text)
    parsed["extracted_text"] = text.strip()
    return parsed
