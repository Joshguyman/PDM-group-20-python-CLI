import psycopg

def create_user(conn, uid, username, password, firstname, lastname):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "INSERT INTO users (uid, username, password, firstname, lastname) VALUES (%s, %s, %s, %s, %s)",
            (uid, username, password, firstname, lastname)
        )
        conn.commit()
    except psycopg.Error as e:
        print(f"Database error: {e}")
    finally:
        curs.close()

def get_user_by_id(conn, uid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "SELECT uid, username from users WHERE uid = %s", (uid,)
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

def make_collection(conn, uid, vid):
    return None

def follow_user(conn, follower_id, followee_id):
    """user follows another user"""
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()

    # if user tries to follow itself, should return false
    if follower_id == followee_id:
        print("Cannot follow yourself.")
        return False

    # what if user already follows user

    try:
        curs.execute(
            "INSERT INTO user_follows_user (follower, followee) VALUES (%s, %s);",
            (follower_id, followee_id)
        )
        conn.commit()
        print("executed statement")
        return True
    except psycopg.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        curs.close()

def unfollow_user(conn, follower_id, followee_id):
    """user unfollows another user"""
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()

    try:
        curs.execute(
            "DELETE FROM user_follows_user WHERE follower= %s and followee = %s;",
            (follower_id, followee_id)
        )
        if curs.rowcount == 0: # row count returns how many rows are deleted.
            print("You do not follow this person")
            return False

        conn.commit()
        print("executed statement")
        return True
    except psycopg.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        curs.close()

def get_following_list(conn, follower_id):
    """Get list of following UID"""
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "SELECT followee from user_follows_user WHERE follower = %s", (follower_id,)
        )
        following = [row[0] for row in curs.fetchall()]

        if not following:
            return []
    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None

def get_follower_list(conn, followee_id):
    """Get list of follower UIDs"""
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "SELECT follower from user_follows_user WHERE followee = %s", (followee_id,)
        )
        follower = [row[0] for row in curs.fetchall()]

        if not follower:
            return []
    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None

