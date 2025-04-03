import psycopg
from .collection_model import create_collection

def create_user(conn: psycopg.Connection, username, password, firstname, lastname, email):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "INSERT INTO users (username, password, firstname, lastname) VALUES (%s, %s, %s, %s) RETURNING uid",
            ( username, password, firstname, lastname)
        )
        uid = curs.fetchone()[0]
        curs.execute(
            "INSERT INTO email (uid, email) VALUES (%s, %s)", (uid, email)
        )
        conn.commit()
        curs.close()
        return uid
    except Exception:
        curs.close()
        return None

def add_email(conn: psycopg.Connection, uid, email):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "INSERT INTO email (uid, email) VALUES (%s, %s)", (uid, email)
        )
        conn.commit()
    except Exception:
        curs.close()
        return None
    finally:
        curs.close()

def get_user_password(conn, uid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "SELECT password from users WHERE uid = %s", (uid,)
        )
        password = curs.fetchone()
        curs.close()
        return password

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None

def get_user_by_id(conn, uid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "SELECT uid, username, password from users WHERE uid = %s", (uid,)
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


"""
update_last_access: changes corresponding lastaccess value in users table
@:param conn -> connection
@:param uid -> id of user accessing
@:param access -> access time by user
@:return -> none
"""


def update_last_access(conn, uid, access):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "UPDATE users SET lastaccess = %s WHERE uid = %s", (access, uid,))
        curs.execute(
            "INSERT INTO user_platform_access (uid, timeaccessed) VALUES (%s, %s)", (uid, access,))
        conn.commit()
        curs.close()
        return

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return

def add_platform_to_user(conn, uid, pid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "INSERT INTO user_owns_platform (uid, pid) VALUES (%s, %s) RETURNING pid", (uid, pid,))
        conn.commit()
        pid = curs.fetchone()
        curs.close()
        return pid
    except Exception as e:
        print(e)
        curs.close()
        return None

def get_platform_by_id(conn, pid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "SELECT name FROM platforms WHERE pid = %s", (pid,)
        )
        name = curs.fetchone()
        curs.close()
        return name
    except Exception:
        curs.close()
        return None

def check_user_platform(conn, uid, pid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute("SELECT pid FROM user_owns_platform WHERE uid = %s AND pid = %s", (uid, pid))
        pid = curs.fetchone()
        curs.close()
        return pid
    except Exception:
        curs.close()
        return None

def get_user_platforms(conn, uid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "SELECT pid FROM user_owns_platform WHERE uid = %s", (uid,))
        pids = curs.fetchall()
        curs.close()
        return pids
    except Exception:
        curs.close()
        return None

def get_user_followers(conn, uid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "SELECT followee FROM user_follows_user WHERE follower = %s", (uid,))
        result = curs.fetchall()
        followees = [row[0] for row in result]
        curs.close()
        return followees
    except Exception:
        curs.close()
        return None

def get_user_videogame_plays(conn, uid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "SELECT vid FROM user_plays_videogame WHERE uid = %s", (uid,))
        result = curs.fetchall()
        games = [row[0] for row in result]
        curs.close()
        return games
    except Exception:
        curs.close()
        return None

