import psycopg
from .collection_model import create_collection

def create_user(conn, username, password, firstname, lastname):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "INSERT INTO users (username, password, firstname, lastname) VALUES (%s, %s, %s, %s)",
            ( username, password, firstname, lastname)
        )
        conn.commit()
    except psycopg.Error as e:
        print(f"Database error: {e}")
    finally:
        curs.close()

def get_user_by_id(conn, uid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "SELECT uid, username from users WHERE uid = %s", (uid,)
        )
        print("executed statement")
        user = curs.fetchone()
        curs.close()
        return user

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None


def get_user_by_username(conn, username):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "SELECT uid, username from users WHERE username = %s", (username,)
        )
        print("executed statement")
        user = curs.fetchone()
        curs.close()
        return user

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None

      
def get_user_by_email(conn, email):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "SELECT u.uid, u.username FROM users u JOIN email e ON u.uid = e.uid WHERE e.email = %s", (email,)
        )
        print("executed statement")
        user = curs.fetchone()
        curs.close()
        return user

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None

def add_collection(conn, colid, name, uid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    create_collection(conn, colid, name, uid)
    curs = conn.cursor()
    try:
        curs.execute(
            "INSERT INTO user_makes_collection (colid, uid) Values (%s, %s)", (colid, uid)
        )
        print("executed statement")
        conn.commit()
        curs.close()
    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None
