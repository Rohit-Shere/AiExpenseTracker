from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# ==============================
# App Init
# ==============================
app = FastAPI(title="AI Expense Tracker – Demo Mode")

# ==============================
# CORS
# ==============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # demo only
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==============================
# WELCOME
# ==============================
@app.get("/")
async def welcome():
    return {"message": "AI Expense Tracker Backend (DEMO MODE)"}


# ==============================
# CHATBOT
# ==============================
class ChatbotRequest(BaseModel):
    user_id: str
    user_input: str

@app.post("/ai/chat")
async def chatbot_interaction(request: ChatbotRequest):
    from backend.chatbot import get_chatbot_response

    response = get_chatbot_response(
        request.user_id,
        request.user_input
    )
    return {"response": response}


# ==============================
# MEMORY
# ==============================
@app.get("/memory")
async def get_memory(user_id: str):
    from backend.memory import fetch_memories_by_user

    memories = fetch_memories_by_user(user_id)
    return {"memories": memories}


# ==============================
# EXPENSE MODELS
# ==============================
class ExpenseCreate(BaseModel):
    user_id: str
    date: str
    category: str
    amount: float
    description: Optional[str] = None


# ==============================
# GET ALL EXPENSES
# ==============================
@app.get("/expenses")
async def get_all_expenses(
    user_id: str = Query(...),
    start_date: str = Query(None),
    end_date: str = Query(None)
):
    from backend.expense import fetch_expense, fetch_expenses_between_dates

    if start_date and end_date:
        expenses = fetch_expenses_between_dates(user_id, start_date, end_date)
    else:
        expenses = fetch_expense(user_id)

    expense_list = [
        {
            "id": e[0],
            "date": e[2],
            "category": e[3],
            "amount": e[4],
            "description": e[5] if len(e) > 5 else None
        }
        for e in expenses
    ]

    return {"expenses": expense_list, "count": len(expense_list)}


# ==============================
# ADD EXPENSE
# ==============================
@app.post("/expenses")
async def add_expense(data: ExpenseCreate):
    from backend.expense import insert_expense

    insert_expense(data.user_id, data)
    return {"message": "Expense added successfully"}


# ==============================
# LATEST EXPENSE
# ==============================
@app.get("/expenses/latest")
async def get_latest_expense(user_id: str):
    from backend.expense import fetch_latest_expense

    expense = fetch_latest_expense(user_id)
    if not expense:
        return {"expense": None}

    return {
        "expense": {
            "id": expense[0],
            "date": expense[2],
            "category": expense[3],
            "amount": expense[4],
            "description": expense[5] if len(expense) > 5 else None
        }
    }


# ==============================
# ANALYTICS – CATEGORY
# ==============================
@app.get("/analytics/category-breakdown")
async def category_breakdown(
    user_id: str = Query(...),
    start_date: str = Query(None),
    end_date: str = Query(None)
):
    from backend.expense import fetch_category_summary

    summary = fetch_category_summary(user_id, start_date, end_date)

    return {
        "summary": [
            {"category": s[0], "total": s[1], "count": s[2]}
            for s in summary
        ]
    }


# ==============================
# DAILY SPENDING
# ==============================
@app.get("/expenses/daily-spending")
async def daily_spending(
    user_id: str,
    start_date: str = Query(None),
    end_date: str = Query(None)
):
    from backend.expense import fetch_daily_spending

    data = fetch_daily_spending(user_id, start_date, end_date)

    return {
        "data": [
            {"date": d[0], "total_amount": d[1] or 0}
            for d in data
        ]
    }


# ==============================
# MONTHLY SPENDING
# ==============================
@app.get("/expenses/monthly-spending")
async def monthly_spending(
    user_id: str,
    start_date: str = Query(None),
    end_date: str = Query(None)
):
    from backend.expense import fetch_monthly_spending

    data = fetch_monthly_spending(user_id, start_date, end_date)

    return {
        "data": [
            {"month": m[0], "total_amount": m[1] or 0}
            for m in data
        ]
    }

class ExpenseUpdate(BaseModel):
    user_id: str
    date: str
    category: str
    amount: float
    description: Optional[str] = None


@app.put("/expenses/{expense_id}")
async def update_expense(
    expense_id: int,
    data: ExpenseUpdate
):
    from backend.expense import update_expense_by_id

    update_expense_by_id(
        expense_id=expense_id,
        user_id=data.user_id,
        date=data.date,
        category=data.category,
        amount=data.amount,
        description=data.description
    )

    return {"message": "Expense updated successfully"}


@app.delete("/expenses/{expense_id}")
async def delete_expense(
    expense_id: int,
    user_id: str = Query(...)
):
    from backend.expense import delete_expense_by_id

    delete_expense_by_id(expense_id, user_id)
    return {"message": "Expense deleted successfully"}
