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