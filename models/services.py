# from db.databse import get_connection


# def get_user(email: str):
#     """Get user from database by email"""
#     conn = get_connection()
#     try:
#         user = conn.execute(
#             "SELECT * FROM users WHERE email = ?",
#             (email,)
#         ).fetchone()
#         return dict(user) if user else None
#     finally:
#         conn.close()


# def create_user(email: str, password_hash: str):
#     """Create a new user in the database"""
#     conn = get_connection()
#     try:
#         cursor = conn.execute(
#             "INSERT INTO users (email, password_hash) VALUES (?, ?)",
#             (email, password_hash)
#         )
#         conn.commit()
#         return cursor.lastrowid
#     finally:
#         conn.close()
from db.databse import get_connection


def get_user(email: str):
    """Get user from database by email"""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )
        user = cur.fetchone()
        return user if user else None
    finally:
        cur.close()
        conn.close()


def create_user(email: str, password_hash: str):
    """Create a new user in the database"""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO users (email, password_hash)
            VALUES (%s, %s)
            RETURNING id
            """,
            (email, password_hash)
        )
        user_id = cur.fetchone()["id"]
        conn.commit()
        return user_id
    finally:
        cur.close()
        conn.close()
