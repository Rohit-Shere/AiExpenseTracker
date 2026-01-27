import sqlite3

DB_PATH = "database/expense.db"

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


# =========================
# Database setup
# =========================
def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            date TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            description TEXT
        );
    """)
    conn.commit()
    conn.close()


# =========================
# CRUD operations
# =========================
def insert_expenses(user_id, date, category, amount, description):
    create_table()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expenses (user_id, date, category, amount, description) VALUES (?, ?, ?, ?, ?)",
        (user_id, date, category, amount, description)
    )
    conn.commit()
    conn.close()


def fetch_expense(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses WHERE user_id=?", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def fetch_expenses_between_dates(user_id, start_date, end_date):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM expenses WHERE user_id=? AND date BETWEEN ? AND ?",
        (user_id, start_date, end_date)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def fetch_latest_expense(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM expenses WHERE user_id=? ORDER BY date DESC, id DESC LIMIT 1",
        (user_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row


def update_expense(expense_id, user_id, amount, category, description):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE expenses
        SET amount=?, category=?, description=?
        WHERE id=? AND user_id=?
    """, (amount, category, description, expense_id, user_id))
    conn.commit()
    conn.close()


def delete_expense(expense_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM expenses WHERE id=? AND user_id=?",
        (expense_id, user_id)
    )
    conn.commit()
    conn.close()


# =========================
# Analytics
# =========================
def fetch_category_summary(user_id, start_date=None, end_date=None):
    conn = get_connection()
    cursor = conn.cursor()

    if start_date and end_date:
        cursor.execute("""
            SELECT category, SUM(amount), COUNT(*)
            FROM expenses
            WHERE user_id=? AND date BETWEEN ? AND ?
            GROUP BY category
        """, (user_id, start_date, end_date))
    else:
        cursor.execute("""
            SELECT category, SUM(amount), COUNT(*)
            FROM expenses
            WHERE user_id=?
            GROUP BY category
        """, (user_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows


def fetch_daily_spending(user_id, start_date=None, end_date=None):
    conn = get_connection()
    cursor = conn.cursor()

    if start_date and end_date:
        cursor.execute("""
            SELECT date, SUM(amount)
            FROM expenses
            WHERE user_id=? AND date BETWEEN ? AND ?
            GROUP BY date
        """, (user_id, start_date, end_date))
    else:
        cursor.execute("""
            SELECT date, SUM(amount)
            FROM expenses
            WHERE user_id=?
            GROUP BY date
        """ ,(user_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows


def fetch_monthly_spending(user_id, start_date=None, end_date=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT strftime('%Y-%m', date), SUM(amount)
        FROM expenses
        WHERE user_id=?
        GROUP BY strftime('%Y-%m', date)
    """, (user_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows


if __name__ == "__main__":
    create_table()
