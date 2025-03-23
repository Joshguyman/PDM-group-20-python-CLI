import psycopg


def follow_user(conn, follower_id, followee_id):
    """user follows another user"""
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()

    # if user tries to follow itself, should return false
    if follower_id == followee_id:
        print("Cannot follow yourself.")
        return False

    try:
        curs.execute(
            "INSERT INTO user_follows_user (follower, followee) VALUES (%s, %s);",
            (follower_id, followee_id)
        )
        conn.commit()
        return True
    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return False


def unfollow_user(conn, follower_id, followee_id):
    """user unfollows another user"""
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")

    try:
        curs = conn.cursor()
        # Check if the relationship exists first
        curs.execute(
            "SELECT 1 FROM user_follows_user WHERE follower = %s AND followee = %s",
            (follower_id, followee_id)
        )
        if not curs.fetchone():
            print("You do not follow this person")
            return False

        curs.execute(
            "DELETE FROM user_follows_user WHERE follower = %s AND followee = %s",
            (follower_id, followee_id)
        )
        conn.commit()
        return True

    except psycopg.Error as e:
        print(f"Database error: {e}")
        return False


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

        return following
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
        followers = [row[0] for row in curs.fetchall()]

        if not followers:
            return []

        return followers
    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None
