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
      
      
def get_similar_user_recs(conn, uid, num=5):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute("""SELECT other.vid, COUNT(*) AS popularity
FROM user_plays_videogame AS other
WHERE other.uid IN (
    SELECT other.uid
    FROM user_plays_videogame AS target
    JOIN user_plays_videogame AS other
      ON target.vid = other.vid
    WHERE target.uid = %s
      AND other.uid != %s
    GROUP BY other.uid
)
AND other.vid NOT IN (
    SELECT vid FROM user_plays_videogame WHERE uid = %s
)
GROUP BY other.vid
ORDER BY popularity DESC
LIMIT %s""", (uid, uid, uid, num))
        vids = curs.fetchall()
        return vids
    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None

def get_similar_games_by_genre(conn, uid, num=5):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute("""SELECT vg.vid, g.name, ROUND(AVG(urv.score), 0) AS average_score
FROM videogame_genre vg
JOIN genre g ON vg.gid = g.gid
JOIN user_rates_videogame urv ON vg.vid = urv.vid
WHERE vg.gid IN (
    SELECT DISTINCT vg2.gid
    FROM user_plays_videogame upv
    JOIN videogame_genre vg2 ON upv.vid = vg2.vid
    WHERE upv.uid = %s
)
AND vg.vid NOT IN (
    SELECT vid FROM user_plays_videogame
    WHERE uid = %s
)
GROUP BY vg.vid, g.name
ORDER BY average_score DESC
LIMIT %s;""", (uid, uid, num))
        vids = curs.fetchall()
        return vids
    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None

def get_similar_games_by_dev(conn, uid, num=5):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute("""SELECT cdv.vid, c.name, ROUND(AVG(urv.score), 2) AS average_score
FROM contributor_develops_videogame cdv
JOIN contributor c ON cdv.conid = c.conid
JOIN user_rates_videogame urv ON cdv.vid = urv.vid
WHERE cdv.conid IN (
    SELECT DISTINCT cdv2.conid
    FROM user_plays_videogame upv
    JOIN contributor_develops_videogame cdv2 ON upv.vid = cdv2.vid
    WHERE upv.uid = %s
)
AND cdv.vid NOT IN (
    SELECT vid FROM user_plays_videogame
    WHERE uid = %s
)
GROUP BY cdv.vid, c.name
ORDER BY average_score DESC
LIMIT %s;""", (uid, uid, num))
        vids = curs.fetchall()
        return vids
    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None

def get_similar_games_by_plat(conn, uid, num=5):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute("""SELECT pcv.vid, ROUND(AVG(urv.score), 2) AS average_score
FROM platform_contains_videogame pcv
JOIN user_rates_videogame urv ON pcv.vid = urv.vid
WHERE pcv.pid IN (
    SELECT DISTINCT pcv2.pid
    FROM user_plays_videogame upv
    JOIN platform_contains_videogame pcv2 ON upv.vid = pcv2.vid
    WHERE upv.uid = %s
)
AND pcv.vid NOT IN (
    SELECT vid FROM user_plays_videogame
    WHERE uid = %s
)
GROUP BY pcv.vid
ORDER BY average_score DESC
LIMIT %s;""", (uid, uid, num))
        vids = curs.fetchall()
        return vids
    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None

def get_similar_games_by_rat(conn, uid, num=5):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute("""WITH user_avg_scores AS (
    SELECT ROUND(AVG(urv.score)) AS rounded_score
    FROM user_plays_videogame upv
    JOIN user_rates_videogame urv ON upv.vid = urv.vid
    WHERE upv.uid = %s
    GROUP BY upv.vid
),
candidate_games AS (
    SELECT urv.vid, ROUND(AVG(urv.score)) AS rounded_score
    FROM user_rates_videogame urv
    GROUP BY urv.vid
)
SELECT vg.vid, cg.rounded_score
FROM candidate_games cg
JOIN videogame vg ON cg.vid = vg.vid
WHERE cg.rounded_score IN (
    SELECT DISTINCT rounded_score FROM user_avg_scores
)
AND vg.vid NOT IN (
    SELECT vid FROM user_plays_videogame
    WHERE uid = %s
)
ORDER BY rounded_score DESC
LIMIT %s;""", (uid, uid, num))
        vids = curs.fetchall()
        return vids
    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None