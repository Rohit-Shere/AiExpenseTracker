from langchain.tools import tool

# Import ONLY pure DB functions
from backend.expense import (
    insert_expenses,
    fetch_expense,
    fetch_expenses_between_dates,
    fetch_category_summary,
    fetch_latest_expense,
    fetch_daily_spending,
    fetch_monthly_spending,
    delete_expense,
    update_expense
)

# =========================
# Expense Tools (AI ONLY)
# =========================

@tool
def insert_expense(user_id: str, date: str, category: str, amount: float, description: str = ""):
    """
    Add a new expense for the user.
    """
    insert_expenses(user_id, date, category, amount, description)
    return "Expense added successfully."


@tool
def fetch_expenses_tool(user_id: str):
    """
    Fetch all expenses for a user.
    """
    return fetch_expense(user_id)


@tool
def fetch_expenses_between_dates_tool(user_id: str, start_date: str, end_date: str):
    """
    Fetch expenses between two dates.
    """
    return fetch_expenses_between_dates(user_id, start_date, end_date)


@tool
def fetch_latest_expense_tool(user_id: str):
    """
    Fetch the most recent expense.
    """
    return fetch_latest_expense(user_id)


@tool
def update_expense_tool(
    expense_id: int,
    user_id: str,
    amount: float,
    category: str,
    description: str = ""
):
    """
    Update an existing expense.
    """
    update_expense(expense_id, user_id, amount, category, description)
    return "Expense updated successfully."


@tool
def delete_expense_tool(expense_id: int, user_id: str):
    """
    Delete an expense.
    """
    delete_expense(expense_id, user_id)
    return "Expense deleted successfully."


# =========================
# Analytics Tools
# =========================

@tool
def fetch_category_summary_tool(user_id: str, start_date: str = None, end_date: str = None):
    """
    Get expense summary grouped by category.
    """
    return fetch_category_summary(user_id, start_date, end_date)


@tool
def fetch_daily_spending_tool(user_id: str, start_date: str = None, end_date: str = None):
    """
    Get daily spending totals.
    """
    return fetch_daily_spending(user_id, start_date, end_date)


@tool
def fetch_monthly_spending_tool(user_id: str, start_date: str = None, end_date: str = None):
    """
    Get monthly spending totals.
    """
    return fetch_monthly_spending(user_id, start_date, end_date)
