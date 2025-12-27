from backend.database import get_db
from backend.security import hash_password

# =========================
# CREATE USER
# =========================
def create_user(name: str, email: str, password: str):
    conn = get_db()
    cur = conn.cursor()

    hashed_password = hash_password(password)

    cur.execute(
        """
        INSERT INTO users (name, email, password)
        VALUES (%s, %s, %s)
        RETURNING id, name, email
        """,
        (name, email, hashed_password)
    )

    user = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return {
        "id": str(user[0]),
        "name": user[1],
        "email": user[2]
    }

# =========================
# GET USER BY EMAIL
# =========================
def get_user_by_email(email: str):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, name, email, password FROM users WHERE email=%s",
        (email,)
    )

    user = cur.fetchone()
    cur.close()
    conn.close()

    return user  # tuple or None

# =========================
# GET USER BY ID
# =========================
def get_user_by_id(user_id: str):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, name, email FROM users WHERE id=%s",
        (user_id,)
    )

    user = cur.fetchone()
    cur.close()
    conn.close()

    return user
