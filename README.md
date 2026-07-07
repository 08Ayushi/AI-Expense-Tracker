# AI Expense Tracker with Receipt OCR

A full-stack personal finance app that lets you track income & expenses, upload
receipts and automatically extract data using **OCR**, auto-categorize spending,
visualise reports with charts, and predict next month's expenses with **machine
learning**.

Built with a **Django REST API** backend and a **React (Vite)** frontend — no
Jinja templates.

> **Note:** The original Flask backend is preserved in `backend/` for reference.
> The active backend is **`backend-django/`**.

---

## Features

- Authentication — register / login / logout with Django sessions + hashed passwords
- Income & Expense tracking — add, list, filter and delete transactions
- Receipt OCR — OpenCV preprocessing + Tesseract extract vendor, date and amount
- Editable extraction — review and edit OCR fields before saving as an expense
- Auto categorization — keyword-based smart category detection
- Dashboard — totals, monthly spending, category chart, recent transactions, budget warnings (at 80%)
- Budgets — set monthly limits per category
- Reports — monthly, category, income-vs-expense charts (Pandas powered)
- Prediction — next-month expense forecast using scikit-learn Linear Regression
- CSV export of all transactions
- **Django Admin** — manage users, transactions, receipts, budgets at `/admin/`

---

## Tech Stack

**Backend:** Python, Django, Django REST Framework, SQLite, Django sessions, OpenCV, pytesseract, Pandas, scikit-learn

**Frontend:** React.js (Vite), React Router, Axios, Bootstrap, Chart.js

---

## Folder Structure

```
ai-expense-tracker/
├── backend-django/          # Django backend (ACTIVE)
│   ├── manage.py
│   ├── config/                # settings, urls, wsgi
│   ├── accounts/              # custom User model + auth API
│   ├── expenses/              # Transaction, Receipt, Budget models + APIs
│   ├── reports/               # Dashboard + report APIs
│   ├── services/              # OCR, category, reports, prediction logic
│   ├── uploads/               # Uploaded receipt images
│   └── requirements.txt
├── backend/                   # Flask backend (legacy / reference)
└── frontend/                  # React app (unchanged UI)
```

---

## Setup & Run (Windows)

### 1. Django Backend

```cmd
cd ai-expense-tracker\backend-django

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

set TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe

python manage.py migrate
python manage.py seed
python manage.py runserver
```

Backend runs at **http://localhost:8000**

**Django Admin:** http://localhost:8000/admin/  
Create a superuser first:
```cmd
python manage.py createsuperuser
```

### 2. React Frontend

```cmd
cd ai-expense-tracker\frontend
npm install
npm run dev
```

Open **http://localhost:5173**

### Demo Login

```
email:    demo@example.com
password: demo123
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Login |
| POST | `/api/auth/logout` | Logout |
| GET  | `/api/auth/me` | Current user |
| POST | `/api/transactions` | Create transaction |
| GET  | `/api/transactions` | List transactions |
| DELETE | `/api/transactions/<id>` | Delete transaction |
| POST | `/api/receipts/upload` | Upload + OCR a receipt |
| POST | `/api/receipts/save-as-expense` | Save extracted data as expense |
| GET  | `/api/dashboard` | Dashboard summary |
| POST | `/api/budgets` | Create/update budget |
| GET  | `/api/budgets` | List budgets |
| GET  | `/api/reports/monthly` | Monthly report |
| GET  | `/api/reports/category` | Category report |
| GET  | `/api/reports/income-vs-expense` | Income vs expense |
| GET  | `/api/reports/export-csv` | CSV export |
| GET  | `/api/reports/prediction` | Next-month prediction |

---

## Tesseract OCR (Windows)

1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to `C:\Program Files\Tesseract-OCR\tesseract.exe`
3. Set env var before running server:
   ```cmd
   set TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
   ```

---

## Database

SQLite file: `backend-django/expense_tracker.db`  
Created automatically on `python manage.py migrate`.

**Your own data:** Register at `/register` — no need to run `seed` again.

---

## Screenshots

_Add your screenshots here._
