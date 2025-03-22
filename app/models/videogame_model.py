import psycopg




def get_videogame_id(conn, title):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "SELECT vid FROM videogame WHERE title = %s",(title,)
        )
        vid = curs.fetchone()
        curs.close()
        return vid
    except Exception as e:
        print(e)
        curs.close()
        return None
def search_videogame_title(conn, title):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")

    curs = conn.cursor()
    try:
        print("Executing search title")
        curs.execute(
            """SELECT v.vid FROM videogame v WHERE v.title ILIKE %s""", (title,)
        )
        user = curs.fetchone()
        curs.close()
        return user

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None
"""
get_videogame_by_id - gets videogame with given vid
@param conn
@param vid
@return videogames with matching videogame id
"""
def get_videogame_by_id(conn, vid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            """SELECT
    v.title,
    STRING_AGG(DISTINCT p.name, ', ') AS platforms,
    STRING_AGG(DISTINCT ps.name, ', ') AS publishers,
    STRING_AGG(DISTINCT ds.name, ', ') AS developers,
    STRING_AGG(DISTINCT upv.durationplayed::TEXT, ', ') AS playtimes,
    STRING_AGG(urv.score::TEXT, ', ') AS ratings,
    STRING_AGG(DISTINCT g.name, ', ') AS genres,
    v.esrbrating,
    pcv.price
FROM videogame v
    JOIN contributor_develops_videogame cdv ON v.vid = cdv.vid
    JOIN contributor_publishes_videogame cpv ON v.vid = cpv.vid
    LEFT JOIN user_plays_videogame upv ON v.vid = upv.vid
    LEFT JOIN user_rates_videogame urv ON v.vid = urv.vid
    JOIN platform_contains_videogame pcv ON v.vid = pcv.vid
    JOIN platform p ON p.pid = pcv.pid
    JOIN videogame_genre vg ON vg.vid = v.vid
    JOIN genre g ON g.gid = vg.gid
    JOIN contributor ps ON ps.conid = cpv.conid
    JOIN contributor ds ON ds.conid = cdv.conid
WHERE v.vid = %s
GROUP BY v.title, v.esrbrating, pcv.price
ORDER BY v.title""", (vid,)
        )
        print("executed statement")
        user = curs.fetchone()
        curs.close()
        return user

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None


"""
get_videogame_by_title - gets videogame with game title
@param conn
@param title
@return videogames with matching game title
"""
def get_videogame_by_title(conn, title):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            """SELECT
    v.title,
    STRING_AGG(DISTINCT p.name, ', ') AS platforms,
    STRING_AGG(DISTINCT ps.name, ', ') AS publishers,
    STRING_AGG(DISTINCT ds.name, ', ') AS developers,
    STRING_AGG(DISTINCT upv.durationplayed::TEXT, ', ') AS playtimes,
    STRING_AGG(urv.score::TEXT, ', ') AS ratings,
    STRING_AGG(DISTINCT g.name, ', ') AS genres,
    v.esrbrating,
    MAX(pcv.price)
FROM videogame v
    JOIN contributor_develops_videogame cdv ON v.vid = cdv.vid
    JOIN contributor_publishes_videogame cpv ON v.vid = cpv.vid
    LEFT JOIN user_plays_videogame upv ON v.vid = upv.vid
    LEFT JOIN user_rates_videogame urv ON v.vid = urv.vid
    JOIN platform_contains_videogame pcv ON v.vid = pcv.vid
    JOIN platform p ON p.pid = pcv.pid
    JOIN videogame_genre vg ON vg.vid = v.vid
    JOIN genre g ON g.gid = vg.gid
    JOIN contributor ps ON ps.conid = cpv.conid
    JOIN contributor ds ON ds.conid = cdv.conid
WHERE v.title ILIKE %s
GROUP BY v.title, v.esrbrating
ORDER BY v.title""", (title,)
        )
        print("executed statement")
        user = curs.fetchall()
        curs.close()
        return user

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None


"""
get_videogame_by_platform_id - gets videogame with given platform id
@param conn
@param pid
@return videogames with matching platform id
"""
def get_videogame_by_platform_id(conn, pid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            """SELECT
    v.title,
    STRING_AGG(DISTINCT p.name, ', ') AS platforms,
    STRING_AGG(DISTINCT ps.name, ', ') AS publishers,
    STRING_AGG(DISTINCT ds.name, ', ') AS developers,
    STRING_AGG(DISTINCT upv.durationplayed::TEXT, ', ') AS playtimes,
    STRING_AGG(urv.score::TEXT, ', ') AS ratings,
    STRING_AGG(DISTINCT g.name, ', ') AS genres,
    v.esrbrating,
    MAX(pcv.price)
FROM videogame v
    JOIN contributor_develops_videogame cdv ON v.vid = cdv.vid
    JOIN contributor_publishes_videogame cpv ON v.vid = cpv.vid
    LEFT JOIN user_plays_videogame upv ON v.vid = upv.vid
    LEFT JOIN user_rates_videogame urv ON v.vid = urv.vid
    JOIN platform_contains_videogame pcv ON v.vid = pcv.vid
    JOIN platform p ON p.pid = pcv.pid
    JOIN videogame_genre vg ON vg.vid = v.vid
    JOIN genre g ON g.gid = vg.gid
    JOIN contributor ps ON ps.conid = cpv.conid
    JOIN contributor ds ON ds.conid = cdv.conid
WHERE p.pid = %s
GROUP BY v.title, v.esrbrating
ORDER BY v.title""", (pid,))
        print("Executed Statement")
        list = curs.fetchall()
        curs.close()
        return list

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None


"""
get_videogame_by_platform - gets videogame with given platform title
@param conn
@param ptitle
@return videogames with matching platform title
"""
def get_videogame_by_platform(conn, ptitle):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute("""SELECT
    v.title,
    STRING_AGG(DISTINCT p.name, ', ') AS platforms,
    STRING_AGG(DISTINCT ps.name, ', ') AS publishers,
    STRING_AGG(DISTINCT ds.name, ', ') AS developers,
    STRING_AGG(DISTINCT upv.durationplayed::TEXT, ', ') AS playtimes,
    STRING_AGG(urv.score::TEXT, ', ') AS ratings,
    STRING_AGG(DISTINCT g.name, ', ') AS genres,
    v.esrbrating,
    MAX(pcv.price)
FROM videogame v
    JOIN contributor_develops_videogame cdv ON v.vid = cdv.vid
    JOIN contributor_publishes_videogame cpv ON v.vid = cpv.vid
    LEFT JOIN user_plays_videogame upv ON v.vid = upv.vid
    LEFT JOIN user_rates_videogame urv ON v.vid = urv.vid
    JOIN platform_contains_videogame pcv ON v.vid = pcv.vid
    JOIN platform p ON p.pid = pcv.pid
    JOIN videogame_genre vg ON vg.vid = v.vid
    JOIN genre g ON g.gid = vg.gid
    JOIN contributor ps ON ps.conid = cpv.conid
    JOIN contributor ds ON ds.conid = cdv.conid
GROUP BY v.title, v.esrbrating
HAVING STRING_AGG(DISTINCT p.name, ', ') ILIKE %s
ORDER BY v.title ASC""", (f"%{ptitle}%",))
        print("Executed Statement")
        vlist = curs.fetchall()
        curs.close()
        return vlist

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None


"""
get_videogame_by_release_date - gets videogame with given release date
@param conn
@param re_date
@return videogames with matching release date
"""
def get_videogame_by_release_date(conn, re_date):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute("""SELECT
    v.title,
    STRING_AGG(DISTINCT p.name, ', ') AS platforms,
    STRING_AGG(DISTINCT ps.name, ', ') AS publishers,
    STRING_AGG(DISTINCT ds.name, ', ') AS developers,
    STRING_AGG(DISTINCT upv.durationplayed::TEXT, ', ') AS playtimes,
    STRING_AGG(urv.score::TEXT, ', ') AS ratings,
    STRING_AGG(DISTINCT g.name, ', ') AS genres,
    v.esrbrating,
    MAX(pcv.price)
FROM videogame v
    JOIN contributor_develops_videogame cdv ON v.vid = cdv.vid
    JOIN contributor_publishes_videogame cpv ON v.vid = cpv.vid
    LEFT JOIN user_plays_videogame upv ON v.vid = upv.vid
    LEFT JOIN user_rates_videogame urv ON v.vid = urv.vid
    JOIN platform_contains_videogame pcv ON v.vid = pcv.vid
    JOIN platform p ON p.pid = pcv.pid
    JOIN videogame_genre vg ON vg.vid = v.vid
    JOIN genre g ON g.gid = vg.gid
    JOIN contributor ps ON ps.conid = cpv.conid
    JOIN contributor ds ON ds.conid = cdv.conid
WHERE v.releasedate = %s
GROUP BY v.title, v.esrbrating
ORDER BY v.title""", (re_date,))
        print("Executed Statement")
        user = curs.fetchall()
        curs.close()
        return user

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None


"""
get_videogame_by_dev_id - gets videogame with given developer id
@param conn
@param conid
@return videogames with matching developer id 
"""
def get_videogame_by_dev_id(conn, conid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute("""SELECT
    v.title,
    STRING_AGG(DISTINCT p.name, ', ') AS platforms,
    STRING_AGG(DISTINCT ps.name, ', ') AS publishers,
    STRING_AGG(DISTINCT ds.name, ', ') AS developers,
    STRING_AGG(DISTINCT upv.durationplayed::TEXT, ', ') AS playtimes,
    STRING_AGG(urv.score::TEXT, ', ') AS ratings,
    STRING_AGG(DISTINCT g.name, ', ') AS genres,
    v.esrbrating,
    MAX(pcv.price)
FROM videogame v
    JOIN contributor_develops_videogame cdv ON v.vid = cdv.vid
    JOIN contributor_publishes_videogame cpv ON v.vid = cpv.vid
    LEFT JOIN user_plays_videogame upv ON v.vid = upv.vid
    LEFT JOIN user_rates_videogame urv ON v.vid = urv.vid
    JOIN platform_contains_videogame pcv ON v.vid = pcv.vid
    JOIN platform p ON p.pid = pcv.pid
    JOIN videogame_genre vg ON vg.vid = v.vid
    JOIN genre g ON g.gid = vg.gid
    JOIN contributor ps ON ps.conid = cpv.conid
    JOIN contributor ds ON ds.conid = cdv.conid
WHERE cdv.conid = %s
GROUP BY v.title, v.esrbrating
ORDER BY v.title""", (conid,))
        print("Executed Statement")
        vlist = curs.fetchall()
        curs.close()
        return vlist

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None


"""
get_videogame_by_dev_name - gets videogame with given developer name
@param conn
@param dname
@return videogames with matching developer name
"""
def get_videogame_by_dev_name(conn, dname):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute("""SELECT
    v.title,
    STRING_AGG(DISTINCT p.name, ', ') AS platforms,
    STRING_AGG(DISTINCT ps.name, ', ') AS publishers,
    STRING_AGG(DISTINCT ds.name, ', ') AS developers,
    STRING_AGG(DISTINCT upv.durationplayed::TEXT, ', ') AS playtimes,
    STRING_AGG(urv.score::TEXT, ', ') AS ratings,
    STRING_AGG(DISTINCT g.name, ', ') AS genres,
    v.esrbrating,
    MAX(pcv.price)
FROM videogame v
    JOIN contributor_develops_videogame cdv ON v.vid = cdv.vid
    JOIN contributor_publishes_videogame cpv ON v.vid = cpv.vid
    LEFT JOIN user_plays_videogame upv ON v.vid = upv.vid
    LEFT JOIN user_rates_videogame urv ON v.vid = urv.vid
    JOIN platform_contains_videogame pcv ON v.vid = pcv.vid
    JOIN platform p ON p.pid = pcv.pid
    JOIN videogame_genre vg ON vg.vid = v.vid
    JOIN genre g ON g.gid = vg.gid
    JOIN contributor ps ON ps.conid = cpv.conid
    JOIN contributor ds ON ds.conid = cdv.conid
WHERE ds.name ILIKE %s
GROUP BY v.title, v.esrbrating
ORDER BY v.title""", (dname,))
        print("Executed Statement")
        vlist = curs.fetchall()
        curs.close()
        return vlist

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None


"""
get_videogame_by_dev_id - gets videogame with given publisher id
@param conn
@param conid
@return videogames with matching publisher id
"""
def get_videogame_by_pub_id(conn, conid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute("""SELECT
    v.title,
    STRING_AGG(DISTINCT p.name, ', ') AS platforms,
    STRING_AGG(DISTINCT ps.name, ', ') AS publishers,
    STRING_AGG(DISTINCT ds.name, ', ') AS developers,
    STRING_AGG(DISTINCT upv.durationplayed::TEXT, ', ') AS playtimes,
    STRING_AGG(urv.score::TEXT, ', ') AS ratings,
    STRING_AGG(DISTINCT g.name, ', ') AS genres,
    v.esrbrating,
    MAX(pcv.price)
FROM videogame v
    JOIN contributor_develops_videogame cdv ON v.vid = cdv.vid
    JOIN contributor_publishes_videogame cpv ON v.vid = cpv.vid
    LEFT JOIN user_plays_videogame upv ON v.vid = upv.vid
    LEFT JOIN user_rates_videogame urv ON v.vid = urv.vid
    JOIN platform_contains_videogame pcv ON v.vid = pcv.vid
    JOIN platform p ON p.pid = pcv.pid
    JOIN videogame_genre vg ON vg.vid = v.vid
    JOIN genre g ON g.gid = vg.gid
    JOIN contributor ps ON ps.conid = cpv.conid
    JOIN contributor ds ON ds.conid = cdv.conid
WHERE cpv.conid = %s
GROUP BY v.title, v.esrbrating
ORDER BY v.title""", (conid,))
        print("Executed Statement")
        vlist = curs.fetchall()
        curs.close()
        return vlist

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None


"""
get_videogame_by_dev_name - gets videogame with given publisher
@param conn
@param pname
@return videogames with matching publisher name
"""
def get_videogame_by_pub_name(conn, pname):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute("""SELECT
    v.title,
    STRING_AGG(DISTINCT p.name, ', ') AS platforms,
    STRING_AGG(DISTINCT ps.name, ', ') AS publishers,
    STRING_AGG(DISTINCT ds.name, ', ') AS developers,
    STRING_AGG(DISTINCT upv.durationplayed::TEXT, ', ') AS playtimes,
    STRING_AGG(urv.score::TEXT, ', ') AS ratings,
    STRING_AGG(DISTINCT g.name, ', ') AS genres,
    v.esrbrating,
    MAX(pcv.price)
FROM videogame v
    JOIN contributor_develops_videogame cdv ON v.vid = cdv.vid
    JOIN contributor_publishes_videogame cpv ON v.vid = cpv.vid
    LEFT JOIN user_plays_videogame upv ON v.vid = upv.vid
    LEFT JOIN user_rates_videogame urv ON v.vid = urv.vid
    JOIN platform_contains_videogame pcv ON v.vid = pcv.vid
    JOIN platform p ON p.pid = pcv.pid
    JOIN videogame_genre vg ON vg.vid = v.vid
    JOIN genre g ON g.gid = vg.gid
    JOIN contributor ps ON ps.conid = cpv.conid
    JOIN contributor ds ON ds.conid = cdv.conid
WHERE ps.name ILIKE %s
GROUP BY v.title, v.esrbrating
ORDER BY v.title""", (pname,))
        print("Executed Statement")
        vlist = curs.fetchall()
        curs.close()
        return vlist

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None


"""
get_videogame_by_price - gets videogame with given price
@param conn
@param price
@return videogames with matching price
"""
def get_videogame_by_price(conn, price):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute("""SELECT
    v.title,
    STRING_AGG(DISTINCT p.name, ', ') AS platforms,
    STRING_AGG(DISTINCT ps.name, ', ') AS publishers,
    STRING_AGG(DISTINCT ds.name, ', ') AS developers,
    STRING_AGG(DISTINCT upv.durationplayed::TEXT, ', ') AS playtimes,
    STRING_AGG(urv.score::TEXT, ', ') AS ratings,
    STRING_AGG(DISTINCT g.name, ', ') AS genres,
    v.esrbrating,
    MAX(pcv.price)
FROM videogame v
    JOIN contributor_develops_videogame cdv ON v.vid = cdv.vid
    JOIN contributor_publishes_videogame cpv ON v.vid = cpv.vid
    LEFT JOIN user_plays_videogame upv ON v.vid = upv.vid
    LEFT JOIN user_rates_videogame urv ON v.vid = urv.vid
    JOIN platform_contains_videogame pcv ON v.vid = pcv.vid
    JOIN platform p ON p.pid = pcv.pid
    JOIN videogame_genre vg ON vg.vid = v.vid
    JOIN genre g ON g.gid = vg.gid
    JOIN contributor ps ON ps.conid = cpv.conid
    JOIN contributor ds ON ds.conid = cdv.conid
WHERE pcv.price = %s
GROUP BY v.title, v.esrbrating
ORDER BY v.title""", (price,))
        print("Executed Statement")
        user = curs.fetchall()
        curs.close()
        return user

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None


"""
get_videogame_by_genre_id - gets videogame with given gid
@param conn
@param gid
@return videogames with matching genre id
"""
def get_videogame_by_genre_id(conn, gid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute("""SELECT
    v.title,
    STRING_AGG(DISTINCT p.name, ', ') AS platforms,
    STRING_AGG(DISTINCT ps.name, ', ') AS publishers,
    STRING_AGG(DISTINCT ds.name, ', ') AS developers,
    STRING_AGG(DISTINCT upv.durationplayed::TEXT, ', ') AS playtimes,
    STRING_AGG(urv.score::TEXT, ', ') AS ratings,
    STRING_AGG(DISTINCT g.name, ', ') AS genres,
    v.esrbrating,
    MAX(pcv.price)
FROM videogame v
    JOIN contributor_develops_videogame cdv ON v.vid = cdv.vid
    JOIN contributor_publishes_videogame cpv ON v.vid = cpv.vid
    LEFT JOIN user_plays_videogame upv ON v.vid = upv.vid
    LEFT JOIN user_rates_videogame urv ON v.vid = urv.vid
    JOIN platform_contains_videogame pcv ON v.vid = pcv.vid
    JOIN platform p ON p.pid = pcv.pid
    JOIN videogame_genre vg ON vg.vid = v.vid
    JOIN genre g ON g.gid = vg.gid
    JOIN contributor ps ON ps.conid = cpv.conid
    JOIN contributor ds ON ds.conid = cdv.conid
WHERE vg.gid = %s
GROUP BY v.title, v.esrbrating
ORDER BY v.title""", (gid,))
        print("Executed Statement")
        user = curs.fetchall()
        curs.close()
        return user

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None


"""
get_videogame_by_genre_name - gets videogame with given genre name
@param conn
@param gname
@return videogames with matching genre name
"""
def get_videogame_by_genre_name(conn, gname):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute("""SELECT
    v.title,
    STRING_AGG(DISTINCT p.name, ', ') AS platforms,
    STRING_AGG(DISTINCT ps.name, ', ') AS publishers,
    STRING_AGG(DISTINCT ds.name, ', ') AS developers,
    STRING_AGG(DISTINCT upv.durationplayed::TEXT, ', ') AS playtimes,
    STRING_AGG(urv.score::TEXT, ', ') AS ratings,
    STRING_AGG(DISTINCT g.name, ', ') AS genres,
    v.esrbrating,
    MAX(pcv.price)
FROM videogame v
    JOIN contributor_develops_videogame cdv ON v.vid = cdv.vid
    JOIN contributor_publishes_videogame cpv ON v.vid = cpv.vid
    LEFT JOIN user_plays_videogame upv ON v.vid = upv.vid
    LEFT JOIN user_rates_videogame urv ON v.vid = urv.vid
    JOIN platform_contains_videogame pcv ON v.vid = pcv.vid
    JOIN platform p ON p.pid = pcv.pid
    JOIN videogame_genre vg ON vg.vid = v.vid
    JOIN genre g ON g.gid = vg.gid
    JOIN contributor ps ON ps.conid = cpv.conid
    JOIN contributor ds ON ds.conid = cdv.conid
GROUP BY v.title, v.esrbrating
HAVING STRING_AGG(DISTINCT g.name, ', ') ILIKE %s
ORDER BY v.title""", (f"%{gname}%",))
        print("Executed Statement")
        vlist = curs.fetchall()
        curs.close()
        return vlist

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None

def get_videogame_platforms(conn, vid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")

    curs = conn.cursor()
    try:
        curs.execute(
            "SELECT pid FROM platform_contains_videogame WHERE vid = %s",
            (vid,))
        pids = curs.fetchall()
        return pids  # No need to close cursor manually; it will be closed when the function exits
    except Exception as e:
        conn.rollback()  # Roll back the transaction to avoid leaving it in an error state
        return None
    finally:
        curs.close()

