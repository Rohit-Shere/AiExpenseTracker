import sqlite3
from langchain.tools import tool

DB_PATH = "database/budget.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

# Create table
def create_table():
    """Create the budgets table in the database if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    q1 = """CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        month TEXT NOT NULL DEFAULT (
            CASE strftime('%m', 'now')
                WHEN '01' THEN 'January'
                WHEN '02' THEN 'February'
                WHEN '03' THEN 'March'
                WHEN '04' THEN 'April'
                WHEN '05' THEN 'May'
                WHEN '06' THEN 'June'
                WHEN '07' THEN 'July'
                WHEN '08' THEN 'August'
                WHEN '09' THEN 'September'
                WHEN '10' THEN 'October'
                WHEN '11' THEN 'November'
                WHEN '12' THEN 'December'
            END
        ),
        amount REAL NOT NULL
    );"""

    cursor.execute(q1)
    conn.commit()
    conn.close()
    
# Insert budget
def insert_budget(user_id, amount, month=None):
    """Insert a new budget into the budgets table."""
    conn = get_connection()
    cursor = conn.cursor()

    create_table()
    if month is None:
        month = """CASE strftime('%m', 'now')
                WHEN '01' THEN 'January'
                WHEN '02' THEN 'February'
                WHEN '03' THEN 'March'
                WHEN '04' THEN 'April'
                WHEN '05' THEN 'May'
                WHEN '06' THEN 'June'
                WHEN '07' THEN 'July'
                WHEN '08' THEN 'August'
                WHEN '09' THEN 'September'
                WHEN '10' THEN 'October'
                WHEN '11' THEN 'November'
                WHEN '12' THEN 'December'
            END"""
        q2 = f"""INSERT INTO budgets (user_id, month, amount)
                VALUES (?, {month}, ?);"""
        cursor.execute(q2, (user_id, amount))
    else:
        q2 = """INSERT INTO budgets (user_id, month, amount)
                VALUES (?, ?, ?);"""
        cursor.execute(q2, (user_id, month, amount))

    conn.commit()
    conn.close()


# Fetch budgets
def fetch_budgets(user_id):
    """Fetch all budgets."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM budgets WHERE user_id=?;",(user_id,))
    rows = cursor.fetchall()

    conn.close()
    return rows

# update budget

def update_budget(user_id, month, amount):
    """Update budget amount for a specific month."""
    conn = get_connection()
    cursor = conn.cursor()

    q = """UPDATE budgets
           SET amount=?
           WHERE user_id=? AND month=?;"""

    cursor.execute(q, (amount, user_id, month))
    conn.commit()
    conn.close()
    
# delete budget
def delete_budget(user_id, month):
    """Delete budget for a specific month."""
    conn = get_connection()
    cursor = conn.cursor()

    q = """DELETE FROM budgets
           WHERE user_id=? AND month=?;"""

    cursor.execute(q, (user_id, month))
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    # Example usage
    insert_budget("user1", 500)
    print(fetch_budgets("user1"))
    update_budget("user1", "March", 600)
    print(fetch_budgets("user1"))
    delete_budget("user1", "March")
    print(fetch_budgets("user1"))
    