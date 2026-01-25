from fastapi import FastAPI, Query
from backend.chatbot import get_chatbot_response
from fastapi.responses import StreamingResponse
from io import BytesIO
from fastapi import Depends
from pydantic import BaseModel
from backend.auth import get_current_user
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from backend.auth import router as auth_router
import os


app = FastAPI(title="Personal Finance Chatbot API")

# List of allowed origins
origins = [
    # Your Vercel frontend
    "https://expence-tracker1-zeta.vercel.app",
    "https://expence-tracker1.vercel.app",
    
    # Development origins
    "http://localhost:8000",
    "http://localhost:3000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000",
    
    # For testing - you can remove this in production
    "*",  # Allows all origins (for testing only)
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Allowed HTTP methods
    allow_headers=["*"],  # Allowed headers
)
# -- Routes --
# ==============================
app.include_router(auth_router)


# ==============================
# Chatbot Endpoints
# ==============================


# well come endpoint
@app.get("/")
async def welcome():
    return {"message": "Welcome to the Personal Finance Chatbot API!"}



# Define an endpoint for chatbot interaction
class ChatbotRequest(BaseModel):

    user_input: str
# Update your endpoint
@app.post("/ai/chat")
async def chatbot_interaction(user_id:str, request: ChatbotRequest):
    try:
        response = get_chatbot_response(user_id, request.user_input)
        return {"response": response}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"response": f"Sorry, I encountered an error: {str(e)}"}

# @app.post("/chatbot/{user_id}")
# async def chatbot_interaction(user_id: str, user_input: str):
#     response = get_chatbot_response(user_id, user_input)
#     return {"response": response}

# fetch memory for user_id
@app.get("/memory/{user_id}")
async def get_memory(user_id: str):
    from backend.memory import fetch_memories_by_user
    memories = fetch_memories_by_user(user_id)
    return {"memories": memories}


# fetch all expenses
# fetch all expenses - FIXED VERSION
@app.get("/expenses")
async def get_all_expenses(
    start_date: str = Query(None),
    end_date: str = Query(None),
    current_user: dict = Depends(get_current_user)
):
    from backend.expense import fetch_expense, fetch_expenses_between_dates

    user_id = current_user["id"]  # 🔐 from JWT

    try:
        if start_date and end_date:
            expenses = fetch_expenses_between_dates(user_id, start_date, end_date)
        else:
            expenses = fetch_expense(user_id)

        expense_list = []
        for exp in expenses:
            expense_list.append({
                "id": exp[0],
                "date": exp[2],
                "category": exp[3],
                "amount": exp[4],
                "description": exp[5] if len(exp) > 5 else None
            })

        return {"expenses": expense_list, "count": len(expense_list)}

    except Exception as e:
        return {"expenses": [], "error": str(e)}

    from backend.expense import fetch_expense, fetch_expenses_between_dates
    if not user_id:
        return {"expenses": [], "error": "user_id parameter is required"}
    
    try:
        if start_date and end_date:
            expenses = fetch_expenses_between_dates(user_id, start_date, end_date)
        else:
            expenses = fetch_expense(user_id)
        
        # Convert to list of dicts for JSON serialization
        expense_list = []
        for exp in expenses:
            expense_list.append({
                "id": exp[0],
                "user_id": exp[1],
                "date": exp[2],
                "category": exp[3],
                "amount": exp[4],
                "description": exp[5] if len(exp) > 5 else None
            })
        return {"expenses": expense_list, "user_id": user_id, "count": len(expense_list)}
    except Exception as e:
        return {"expenses": [], "error": str(e)}

# Get latest expense
@app.get("/expenses/latest")
async def get_latest_expense(
    current_user: dict = Depends(get_current_user)
    ):
    from backend.expense import fetch_latest_expense

    user_id = current_user["id"]

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

    from backend.expense import fetch_latest_expense
    if not user_id:
        return {"expense": None, "error": "user_id parameter is required"}
    
    try:
        expense = fetch_latest_expense(user_id)
        if expense:
            return {
                "expense": {
                    "id": expense[0],
                    "user_id": expense[1],
                    "date": expense[2],
                    "category": expense[3],
                    "amount": expense[4],
                    "description": expense[5] if len(expense) > 5 else None
                }
            }
        return {"expense": None}
    except Exception as e:
        return {"expense": None, "error": str(e)}

# Get category summary
@app.get("/analytics/category-breakdown")
async def get_category_summary(
    start_date: str = Query(None),
    end_date: str = Query(None),
    current_user: dict = Depends(get_current_user)
    ):
    from backend.expense import fetch_category_summary

    user_id = current_user["id"]
    summary = fetch_category_summary(user_id, start_date, end_date)

    return {
        "summary": [
            {"category": s[0], "total": s[1], "count": s[2]}
            for s in summary
        ]
    }


# Get daily spending data
@app.get("/expenses/daily-spending")
async def get_daily_spending(
    start_date: str = Query(None),
    end_date: str = Query(None),
    current_user: dict = Depends(get_current_user)
    ):
    from backend.expense import fetch_daily_spending

    user_id = current_user["id"]
    data = fetch_daily_spending(user_id, start_date, end_date)

    return {
        "data": [
            {"date": d[0], "total_amount": d[1] or 0}
            for d in data
        ]
    }

# Get monthly spending data
@app.get("/expenses/monthly-spending")
async def get_monthly_spending(
    start_date: str = Query(None),
    end_date: str = Query(None),
    current_user: dict = Depends(get_current_user)
    ):
    from backend.expense import fetch_monthly_spending

    user_id = current_user["id"]
    data = fetch_monthly_spending(user_id, start_date, end_date)

    return {
        "data": [
            {"month": m[0], "total_amount": m[1] or 0}
            for m in data
        ]
    }

# ==============================
# Visualization Endpoints
# ==============================

# @app.get("/visuals/daily_spending/{user_id}")
# async def get_daily_spending_visual(user_id: int):
#     from backend.expense import fetch_daily_spending
#     from backend.visuals import plot_daily_spending
#     # Fetch data
#     data = fetch_daily_spending(user_id)
#     dates = [row[0] for row in data]
#     amounts = [row[1] for row in data]
#     # Generate plot
#     img = plot_daily_spending(dates, amounts)
#     # # Save to a temporary file and return the path
#     # temp_path = f"temp_daily_spending_{user_id}.png"
#     # img.save(temp_path)
#     return img
