import psycopg

def create_collection(conn, name, uid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "INSERT INTO collection (name, uid) VALUES (%s, %s) RETURNING colid",
            (name, uid)
        )
        conn.commit()
        colid =curs.fetchone()[0]
        curs.execute(
            "INSERT INTO user_makes_collection (uid, colid) VALUES (%s, %s)",
            (uid, colid)
        )
        conn.commit()
        curs.close()
        return colid
    except Exception as e:
        print(f"Connection failed: {e}")
        curs.close()
        return None

def get_collection_by_id(conn, colid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "SELECT colid, name from collection WHERE colid = %s", (colid,)
        )
        print("executed statement")
        user = curs.fetchone()
        curs.close()
        return user

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None

def get_collection_by_user(conn, uid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "SELECT colid from user_makes_collection WHERE uid = %s", (uid,)
        )
        colids = [row[0] for row in curs.fetchall()]

        if not colids:
            return []

        curs.execute("SELECT name FROM collection WHERE colid = ANY(%s)", (colids,))
        collection_names = [row[0] for row in curs.fetchall()]

        return collection_names

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None

def get_games_in_collection(conn, colid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    
    curs = conn.cursor()
    try:
        curs.execute(
            """
            SELECT v.title  -- Change 'name' to 'title'
            FROM videogame v
            INNER JOIN collection_contains_videogame ccv ON v.vid = ccv.vid
            WHERE ccv.colid = %s
            """,
            (colid,)
        )
        games = [row[0] for row in curs.fetchall()]
        return games  # Returns a list of game titles
    
    except psycopg.Error as e:
        print(f"Database error: {e}")
        return []
    
    finally:
        curs.close()

def add_game(conn, colid, vid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "INSERT INTO collection_contains_videogame (colid, vid) VALUES (%s, %s)", (colid, vid)
        )
        print("executed statement")
        user = curs.fetchone()
        curs.close()
        return user

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None

