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
        collection = curs.fetchone()[1]
        curs.close()
        return collection

    except Exception:
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
            SELECT v.title 
            FROM videogame v
            INNER JOIN collection_contains_videogame ccv ON v.vid = ccv.vid
            WHERE ccv.colid = %s
            """,
            (colid,)
        )
        games = [row[0] for row in curs.fetchall()]
        return games
    
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
        curs.close()
        conn.commit()
        return
    except psycopg.Error as e:
        print(e)
        curs.close()
        return

def remove_game(conn, colid, vid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "DELETE FROM collection_contains_videogame WHERE vid = %s AND colid = %s", (vid, colid)
        )
        curs.close()
        conn.commit()
        return
    except psycopg.Error as e:
        curs.close()
        return None
    

def get_collection_details(conn, uid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")

    curs = conn.cursor()
    try:
        # Check if the user has collections
        curs.execute("SELECT COUNT(*) FROM collection WHERE uid = %s", (uid,))
        count = curs.fetchone()[0]
        if count == 0:
            return []

        # Run the main query
        curs.execute("""
            SELECT 
                c.name AS collection_name,
                COUNT(ccv.vid) AS game_count,
                COALESCE(
                    TO_CHAR(
                        INTERVAL '1 second' * SUM(
                            (split_part(upv.durationplayed, ':', 1)::INT * 3600) + 
                            (split_part(upv.durationplayed, ':', 2)::INT * 60)
                        ), 
                        'HH24:MI'
                    ), '00:00'
                ) AS total_play_time,
                ARRAY_AGG(upv.durationplayed) AS durations  -- Debugging: Print the durations
            FROM collection c
            LEFT JOIN collection_contains_videogame ccv ON c.colid = ccv.colid
            LEFT JOIN user_plays_videogame upv ON ccv.vid = upv.vid AND upv.uid = %s
            WHERE c.uid = %s
            GROUP BY c.colid, c.name
            ORDER BY c.name ASC;
        """, (uid, uid))

        collections = curs.fetchall()

        # Unpacking the values correctly
        curs.close()
        return collections

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None

def check_collection_owner(conn, uid, colid) -> bool:
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "SELECT uid FROM user_makes_collection WHERE colid = %s", (colid,)
        )
        tmp_uid = curs.fetchone()[0]
        curs.close()
        if(tmp_uid != uid):
            return False
        return True
    except Exception:
        curs.close()
        return False

def check_game_in_collection(conn, colid, vid) -> bool:
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "SELECT vid FROM collection_contains_videogame WHERE colid = %s", (colid,)
        )
        vids = curs.fetchall()
        curs.close()
        if vids is None: return False
        for v in vids:
            if v[0] == vid:
                return True
        return False
    except Exception:
        curs.close()
        return False


def change_collection_name(conn, uid, colid, name):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    if check_collection_owner(conn, uid, colid):
        try:
            curs.execute(
                "UPDATE collection SET name = %s WHERE colid = %s", (name, colid)
            )
            conn.commit()
            curs.close()
            return
        except Exception:
            curs.close()
            return
    else:
        curs.close()
        print("Failed to rename.")
        return

def delete_collection(conn, uid, colid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")

    curs = conn.cursor()
    if check_collection_owner(conn, uid, colid):
        try:
            curs.execute(
                "DELETE FROM user_makes_collection WHERE colid = %s", (colid,))
            conn.commit()
            curs.execute(
                "DELETE FROM collection WHERE colid = %s", (colid,))
            conn.commit()
            curs.close()
            print(f"Collection # {colid} successfully removed.")
            return

        except Exception as e:
            print(f"Deletion failed: {e}")
            conn.rollback()
            curs.close()
            return
    else:
        print("Invalid Collection")
        curs.close()
        return


