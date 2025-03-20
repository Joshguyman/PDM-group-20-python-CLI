import psycopg
from datetime import datetime

def play_video_game(conn, uid, vid, duration):
    """ Record that user played a specific video game for a given duration """

    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "INSERT INTO user_plays_videogame (uid, vid, time_started, duration) VALUES (%s, %s, %s, %s);",
            (uid, vid, datetime.now(), duration)
        )

        conn.commit()
        print("executed statement")
        return True
    except psycopg.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        curs.close()

def play_random_video_game(conn, colid, uid, duration):
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

        return play_video_game(conn, uid, vid, duration)

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return False
    finally:
        curs.close()
