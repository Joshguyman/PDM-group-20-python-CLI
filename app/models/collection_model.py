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
    
import psycopg

def get_collection_details(conn, uid):
    """
    Retrieves all collections owned by a user, including:
    - Collection Name
    - Number of Games in Collection
    - Total Play Time (formatted as HH:MM)

    :param conn: Database connection
    :param uid: User ID
    :return: List of collections with details
    """

    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    
    curs = conn.cursor()
    try:
        curs.execute("""
            SELECT 
                c.name AS collection_name,
                COUNT(ccv.vid) AS game_count,
                COALESCE(
                    TO_CHAR(
                        INTERVAL '1 second' * SUM(upv.duration), 'HH24:MI'
                    ), '00:00'
                ) AS total_play_time
            FROM collection c
            LEFT JOIN collection_contains_videogame ccv ON c.colid = ccv.colid
            LEFT JOIN user_plays_videogame upv ON ccv.vid = upv.vid AND upv.uid = %s
            WHERE c.uid = %s
            GROUP BY c.colid, c.name
            ORDER BY c.name ASC;
        """, (uid, uid))

        collections = curs.fetchall()
        curs.close()

        return collections

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None
