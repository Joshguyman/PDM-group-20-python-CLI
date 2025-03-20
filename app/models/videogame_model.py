import psycopg

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
        p.name,
        ps.name,
        ds.name,
        upv.durationplayed,
        urv.score,
        v.esrbrating
FROM videogame v
    JOIN contributor_develops_videogame cdv ON v.vid = cdv.vid
    JOIN contributor_publishes_videogame cpv ON v.vid = cpv.vid
    JOIN user_plays_videogame upv ON v.vid = upv.vid
    JOIN user_rates_videogame urv ON v.vid = urv.vid
    JOIN platform_contains_videogame pcv ON v.vid = pcv.vid
    JOIN platform p ON p.pid = pcv.pid
    JOIN contributor ps ON ps.conid = cpv.conid
    JOIN contributor ds ON ds.conid = cdv.conid WHERE v.vid = %s""", (vid,)
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
        p.name,
        ps.name,
        ds.name,
        upv.durationplayed,
        urv.score,
        v.esrbrating
FROM videogame v
    JOIN contributor_develops_videogame cdv ON v.vid = cdv.vid
    JOIN contributor_publishes_videogame cpv ON v.vid = cpv.vid
    JOIN user_plays_videogame upv ON v.vid = upv.vid
    JOIN user_rates_videogame urv ON v.vid = urv.vid
    JOIN platform_contains_videogame pcv ON v.vid = pcv.vid
    JOIN platform p ON p.pid = pcv.pid
    JOIN contributor ps ON ps.conid = cpv.conid
    JOIN contributor ds ON ds.conid = cdv.conid WHERE v.title = %s""", (title,)
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
        p.name,
        ps.name,
        ds.name,
        upv.durationplayed,
        urv.score,
        v.esrbrating
FROM videogame v
    JOIN contributor_develops_videogame cdv ON v.vid = cdv.vid
    JOIN contributor_publishes_videogame cpv ON v.vid = cpv.vid
    JOIN user_plays_videogame upv ON v.vid = upv.vid
    JOIN user_rates_videogame urv ON v.vid = urv.vid
    JOIN platform_contains_videogame pcv ON v.vid = pcv.vid
    JOIN platform p ON p.pid = pcv.pid
    JOIN contributor ps ON ps.conid = cpv.conid
    JOIN contributor ds ON ds.conid = cdv.conid WHERE p.pid = %s""", (pid,))
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
        p.name,
        ps.name,
        ds.name,
        upv.durationplayed,
        urv.score,
        v.esrbrating
FROM videogame v
    JOIN contributor_develops_videogame cdv ON v.vid = cdv.vid
    JOIN contributor_publishes_videogame cpv ON v.vid = cpv.vid
    JOIN user_plays_videogame upv ON v.vid = upv.vid
    JOIN user_rates_videogame urv ON v.vid = urv.vid
    JOIN platform_contains_videogame pcv ON v.vid = pcv.vid
    JOIN platform p ON p.pid = pcv.pid
    JOIN contributor ps ON ps.conid = cpv.conid
    JOIN contributor ds ON ds.conid = cdv.conid WHERE p.name = %s""", (ptitle,))
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
        p.name,
        ps.name,
        ds.name,
        upv.durationplayed,
        urv.score,
        v.esrbrating
FROM videogame v
    JOIN contributor_develops_videogame cdv ON v.vid = cdv.vid
    JOIN contributor_publishes_videogame cpv ON v.vid = cpv.vid
    JOIN user_plays_videogame upv ON v.vid = upv.vid
    JOIN user_rates_videogame urv ON v.vid = urv.vid
    JOIN platform_contains_videogame pcv ON v.vid = pcv.vid
    JOIN platform p ON p.pid = pcv.pid
    JOIN contributor ps ON ps.conid = cpv.conid
    JOIN contributor ds ON ds.conid = cdv.conid WHERE pcv.releasedate = %s""", (re_date,))
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
        p.name,
        ps.name,
        ds.name,
        upv.durationplayed,
        urv.score,
        v.esrbrating
FROM videogame v
    JOIN contributor_develops_videogame cdv ON v.vid = cdv.vid
    JOIN contributor_publishes_videogame cpv ON v.vid = cpv.vid
    JOIN user_plays_videogame upv ON v.vid = upv.vid
    JOIN user_rates_videogame urv ON v.vid = urv.vid
    JOIN platform_contains_videogame pcv ON v.vid = pcv.vid
    JOIN platform p ON p.pid = pcv.pid
    JOIN contributor ps ON ps.conid = cpv.conid
    JOIN contributor ds ON ds.conid = cdv.conid WHERE cdv.conid = %s""", (conid,))
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
        p.name,
        ps.name,
        ds.name,
        upv.durationplayed,
        urv.score,
        v.esrbrating
FROM videogame v
    JOIN contributor_develops_videogame cdv ON v.vid = cdv.vid
    JOIN contributor_publishes_videogame cpv ON v.vid = cpv.vid
    JOIN user_plays_videogame upv ON v.vid = upv.vid
    JOIN user_rates_videogame urv ON v.vid = urv.vid
    JOIN platform_contains_videogame pcv ON v.vid = pcv.vid
    JOIN platform p ON p.pid = pcv.pid
    JOIN contributor ps ON ps.conid = cpv.conid
    JOIN contributor ds ON ds.conid = cdv.conid WHERE ds.name = %s""", (dname,))
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
        p.name,
        ps.name,
        ds.name,
        upv.durationplayed,
        urv.score,
        v.esrbrating
FROM videogame v
    JOIN contributor_develops_videogame cdv ON v.vid = cdv.vid
    JOIN contributor_publishes_videogame cpv ON v.vid = cpv.vid
    JOIN user_plays_videogame upv ON v.vid = upv.vid
    JOIN user_rates_videogame urv ON v.vid = urv.vid
    JOIN platform_contains_videogame pcv ON v.vid = pcv.vid
    JOIN platform p ON p.pid = pcv.pid
    JOIN contributor ps ON ps.conid = cpv.conid
    JOIN contributor ds ON ds.conid = cdv.conid WHERE cpv.conid = %s""", (conid,))
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
        p.name,
        ps.name,
        ds.name,
        upv.durationplayed,
        urv.score,
        v.esrbrating
FROM videogame v
    JOIN contributor_develops_videogame cdv ON v.vid = cdv.vid
    JOIN contributor_publishes_videogame cpv ON v.vid = cpv.vid
    JOIN user_plays_videogame upv ON v.vid = upv.vid
    JOIN user_rates_videogame urv ON v.vid = urv.vid
    JOIN platform_contains_videogame pcv ON v.vid = pcv.vid
    JOIN platform p ON p.pid = pcv.pid
    JOIN contributor ps ON ps.conid = cpv.conid
    JOIN contributor ds ON ds.conid = cdv.conid WHERE ps.name = %s""", (pname,))
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
        p.name,
        ps.name,
        ds.name,
        upv.durationplayed,
        urv.score,
        v.esrbrating
FROM videogame v
    JOIN contributor_develops_videogame cdv ON v.vid = cdv.vid
    JOIN contributor_publishes_videogame cpv ON v.vid = cpv.vid
    JOIN user_plays_videogame upv ON v.vid = upv.vid
    JOIN user_rates_videogame urv ON v.vid = urv.vid
    JOIN platform_contains_videogame pcv ON v.vid = pcv.vid
    JOIN platform p ON p.pid = pcv.pid
    JOIN contributor ps ON ps.conid = cpv.conid
    JOIN contributor ds ON ds.conid = cdv.conid WHERE pcv.price = %s""", (price,))
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
        p.name,
        ps.name,
        ds.name,
        upv.durationplayed,
        urv.score,
        v.esrbrating
FROM videogame v
    JOIN contributor_develops_videogame cdv ON v.vid = cdv.vid
    JOIN contributor_publishes_videogame cpv ON v.vid = cpv.vid
    JOIN user_plays_videogame upv ON v.vid = upv.vid
    JOIN user_rates_videogame urv ON v.vid = urv.vid
    JOIN platform_contains_videogame pcv ON v.vid = pcv.vid
    JOIN platform p ON p.pid = pcv.pid
    JOIN genre g ON g.gid = vg.gid
    JOIN videogame_genre vg ON vg.vid = v.vid
    JOIN contributor ps ON ps.conid = cpv.conid
    JOIN contributor ds ON ds.conid = cdv.conid WHERE vg.gid = %s""", (gid,))
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
        p.name,
        ps.name,
        ds.name,
        upv.durationplayed,
        urv.score,
        v.esrbrating
FROM videogame v
    JOIN contributor_develops_videogame cdv ON v.vid = cdv.vid
    JOIN contributor_publishes_videogame cpv ON v.vid = cpv.vid
    JOIN user_plays_videogame upv ON v.vid = upv.vid
    JOIN user_rates_videogame urv ON v.vid = urv.vid
    JOIN platform_contains_videogame pcv ON v.vid = pcv.vid
    JOIN platform p ON p.pid = pcv.pid
    JOIN videogame_genre vg ON vg.vid = v.vid
    JOIN genre g ON g.gid = vg.gid
    JOIN contributor ps ON ps.conid = cpv.conid
    JOIN contributor ds ON ds.conid = cdv.conid WHERE g.name = %s""", (gname,))
        print("Executed Statement")
        vlist = curs.fetchall()
        curs.close()
        return vlist

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None
