import psycopg

def get_videogame_by_id(conn, vid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "SELECT vid, title from videogame WHERE vid = %s", (vid,)
        )
        print("executed statement")
        user = curs.fetchone()
        curs.close()
        return user

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None


def get_videogame_by_title(conn, title):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "SELECT vid, title FROM videogame WHERE title = %s", (title,)
        )
        print("executed statement")
        user = curs.fetchone()
        curs.close()
        return user

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None

def get_videogame_by_platform_id(conn, pid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute("SELECT v.vid, v.title FROM videogame v JOIN platform_contains_videogame p ON p.vid = v.vid WHERE p.pid = %s", (pid,))
        print("Executed Statement")
        list = curs.fetchall()
        curs.close()
        return list

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None


def get_videogame_by_release_date(conn, re_date):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute("SELECT vid from platform_contains_videogame WHERE releasedate = %s", re_date)
        print("Executed Statement")
        user = curs.fetchone()
        curs.close()
        return user

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None
