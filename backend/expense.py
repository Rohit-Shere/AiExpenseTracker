import sqlite3
from langchain.tools import tool

DB_PATH = "database/expense.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# Create table
# @tool
def create_table():
    """Create the expenses table in the database if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    q1 = """CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        description TEXT
    );"""

    cursor.execute(q1)
    conn.commit()
    conn.close()

# Insert expense
@tool
def insert_expense(date, category, amount, description):
    """Insert a new expense into the expenses table."""
    conn = get_connection()
    cursor = conn.cursor()

    create_table()
    q2 = """INSERT INTO expenses (date, category, amount, description)
            VALUES (?, ?, ?, ?);"""

    cursor.execute(q2, (date, category, amount, description))
    conn.commit()
    conn.close()

# Fetch all expenses
def fetch_expense():
    """Fetch all expenses."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses;")
    rows = cursor.fetchall()

    conn.close()
    return rows


@tool
def fetch_expenses():
    """Fetch all expenses."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses;")
    rows = cursor.fetchall()

    conn.close()
    return rows

# Fetch expenses by category
@tool
def fetch_expenses_by_category(category):
    """Fetch expenses by category."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses WHERE category = ?;", (category,))
    rows = cursor.fetchall()

    conn.close()
    return rows

# Fetch total expenses between dates 
@tool
def fetch_total_expenses_between_dates(start_date, end_date):
    """Fetch total expenses between two dates."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT SUM(amount) FROM expenses WHERE date BETWEEN ? AND ?;",
        (start_date, end_date)
    )
    result = cursor.fetchone()

    conn.close()
    return result[0] if result else 0.0

# Fetch expenses between dates 
@tool
def fetch_expenses_between_dates(start_date, end_date):
    """Fetch expenses between two dates."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM expenses WHERE date BETWEEN ? AND ?;",
        (start_date, end_date)
    )
    rows = cursor.fetchall()

    conn.close()
    return rows

if __name__ == "expense":
    create_table()