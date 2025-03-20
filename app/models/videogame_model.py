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
            "SELECT v.vid, v.title FROM videogame v JOIN platform_contains_videogame p ON p.vid = v.vid WHERE p.pid = %s", (pid,))
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
        curs.execute("SELECT v.vid, v.title FROM videogame v JOIN platform_contains_videogame p ON p.vid = v.vid JOIN platform pl ON p.pid = pl.pid WHERE pl.name = %s", (ptitle,))
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
        curs.execute("SELECT v.vid, v.title FROM videogame v JOIN platform_contains_videogame p ON p.vid = v.vid WHERE p.releasedate = %s", (re_date,))
        print("Executed Statement")
        user = curs.fetchall()
        curs.close()
        return user

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None

"""
get_videogame_by_dev_id - gets videogame with given contributor id (devs only)
@param conn
@param conid
@return videogames with matching contributor id (devs only)
"""
def get_videogame_by_dev_id(conn, conid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute("SELECT v.vid, v.title FROM videogame v JOIN contributor_develops_videogame co ON v.vid = co.vid WHERE co.conid = %s", (conid,))
        print("Executed Statement")
        vlist = curs.fetchall()
        curs.close()
        return vlist

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None

"""
get_videogame_by_dev_name - gets videogame with given contributor name (devs only)
@param conn
@param dname
@return videogames with matching contributor name (devs only)
"""
def get_videogame_by_dev_name(conn, dname):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute("SELECT v.vid, v.title FROM videogame v JOIN contributor_develops_videogame con ON con.vid = v.vid JOIN contributor co ON con.conid = co.conid WHERE co.name = %s", (dname,))
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
        curs.execute("SELECT v.vid, v.title FROM videogame v JOIN platform_contains_videogame p ON p.vid = v.vid WHERE p.price = %s", (price,))
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
        curs.execute("SELECT v.vid, v.title FROM videogame v JOIN videogame_genre g ON g.vid = v.vid WHERE g.gid = %s", (gid,))
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
        curs.execute("SELECT v.vid, v.title FROM videogame v JOIN videogame_genre ge ON ge.vid = v.vid JOIN genre gen ON gen.gid = ge.gid WHERE gen.name = %s", (gname,))
        print("Executed Statement")
        vlist = curs.fetchall()
        curs.close()
        return vlist

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None
