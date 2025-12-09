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
    """Fetch expenses by category.
    param category: Category of expenses to fetch"""
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses WHERE category = ?;", (category,))
    rows = cursor.fetchall()

    conn.close()
    return rows

# Fetch total expenses between dates 
@tool
def fetch_total_expenses_between_dates(start_date, end_date):
    """Fetch total expenses between two dates.
    param start_date: Start date in YYYY-MM-DD format
    param end_date: End date in YYYY-MM-DD format"""
    
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
    """Fetch expenses between two dates.
    param start_date: Start date in YYYY-MM-DD format
    param end_date: End date in YYYY-MM-DD format"""
    
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM expenses WHERE date BETWEEN ? AND ?;",
        (start_date, end_date)
    )
    rows = cursor.fetchall()

    conn.close()
    return rows


# Edit expense - Optional Enhancement
@tool
def edit_expense(id, amount=None, category=None, description=None):
    """Edit an existing expense.
    param id: ID of the expense to edit
    param amount: New amount (optional)
    param category: New category (optional)
    param description: New description (optional)
    """
    
    conn = get_connection()
    cursor = conn.cursor()
    cur.execute("""
        UPDATE expenses 
        SET amount=?, category=?, description=? 
        WHERE id=?
    """, (amount, category, description, id))
    conn.commit()
    conn.close()
    
# Delete expense - Optional Enhancement
@tool
def delete_expense(id,date:None):
    """Delete an expense by ID.
    param id: ID of the expense to delete
    param date: Date of the expense to delete (optional)
    """
    conn = get_connection()
    cursor = conn.cursor()
    if date:
        cursor.execute("DELETE FROM expenses WHERE id=? AND date=? ;", (id,date))
    else:
        cursor.execute("DELETE FROM expenses WHERE id=? ;", (id,))
    conn.commit()
    conn.close()


if __name__ == "expense":
    create_table()
    
    
    