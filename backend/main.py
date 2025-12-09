from fastapi import FastAPI
from backend.chatbot import get_chatbot_response
import os


app = FastAPI(title="Personal Finance Chatbot API")

# Define an endpoint for chatbot interaction
@app.post("/chatbot/{user_id}")
async def chatbot_interaction(user_id: str, user_input: str):
    response = get_chatbot_response(user_id, user_input)
    return {"response": response}

# fetch memory for user_id
@app.get("/memory/{user_id}")
async def get_memory(user_id: str):
    from backend.memory import fetch_memories_by_user
    memories = fetch_memories_by_user(user_id)
    return {"memories": memories}

# fetch all expenses
@app.get("/expenses")
async def get_all_expenses():
    from backend.expense import fetch_expense
    expenses = fetch_expense()
    return {"expenses": expenses}