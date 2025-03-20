import psycopg

def create_collection(conn, colid, name, uid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "INSERT INTO collection (colid, name, uid) VALUES (%s, %s, %s)",
            (colid, name, uid)
        )
        conn.commit()
    except psycopg.Error as e:
        print(f"Database error: {e}")
    finally:
        curs.close()

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

def get_collection_details(conn, uid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    
    curs = conn.cursor()
    try:
        curs.execute(
            """
            SELECT c.name, 
                   COUNT(ccv.vid) AS game_count, 
                   COALESCE(SUM(v.durationplayed), 0) AS total_minutes
            FROM collection c
            LEFT JOIN collection_contains_videogame ccv ON c.colid = ccv.colid
            LEFT JOIN videogame v ON ccv.vid = v.vid
            WHERE c.uid = %s
            GROUP BY c.colid, c.name
            ORDER BY c.name ASC;
            """,
            (uid,)
        )

        collections = []
        for row in curs.fetchall():
            collection_name = row[0]
            game_count = row[1]
            minutes = row[2]
            hours = minutes // 60
            minutes = minutes % 60
            playtime = f"{hours}:{minutes:02d}"
            collections.append((collection_name, game_count, playtime))
        
        return collections
    except psycopg.Error as e:
        print(f"Database error: {e}")
        return[]
    finally:
        curs.close()