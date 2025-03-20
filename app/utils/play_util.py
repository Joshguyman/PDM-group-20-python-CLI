import psycopg

def play_video_game(conn, uid, vid, time_started, duration):
    """
    Records that a user has played a video_game
    :param conn: database connection
    :param uid: integer, User ID
    :param vid: integer, Video game ID
    :param time_started: date and time started, in format XXXX-XX-XX XX:XX:XX.XXXXXX
    :param duration: integer, duration user played.
    :return: true, if properly executed.
    """

    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "INSERT INTO user_plays_videogame (uid, vid, time_started, duration) VALUES (%s, %s, %s, %s);",
            (uid, vid, time_started, duration)
        )

        conn.commit()
        print("executed statement")
        return True
    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return False

def play_random_video_game(conn, colid, uid, time_started, duration):
    """ Record that user played a random video game from a collection for a given duration """
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "SELECT vid from collection_contains_videogame WHERE colid = %s ORDER BY RANDOM() LIMIT 1;",
            (colid,)
        )

        game = curs.fetchone()

        if not game:
            print("no games found")
            return False

        vid = game[0]

        return play_video_game(conn, uid, vid, time_started, duration)

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return False
