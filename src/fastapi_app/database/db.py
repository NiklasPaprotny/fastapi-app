import sqlite3
from pathlib import Path
from contextlib import contextmanager

from fastapi_app.models.user import User

DB_FILE = Path(__file__).parents[2] / "data" / "data.db"

if not DB_FILE.exists():
    raise FileNotFoundError(f"Database not found at {DB_FILE}")

@contextmanager
def get_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def get_all_users() -> list[dict]:
    with get_connection() as conn:
        cur = conn.execute("SELECT * FROM users")
        return [dict(row) for row in cur.fetchall()]

def get_user_by_id(user_id: int) -> dict | None:
    with get_connection() as conn:
        cur = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cur.fetchone()
        return dict(user) if user else None

def create_user(user: User) -> dict:
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO users (name, email, age, is_active, street, city, state, zip, tags) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                user.name,
                user.email,
                user.age,
                user.is_active,
                user.street,
                user.city,
                user.state,
                user.zip_code,
                ",".join(user.tags)
            )
        )
        conn.commit()
        return {"id": cur.lastrowid,  **user.model_dump()}

def get_user_by_email(email: str) -> dict | None:
    with get_connection() as conn:
        cur = conn.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cur.fetchone()
        return dict(user) if user else None