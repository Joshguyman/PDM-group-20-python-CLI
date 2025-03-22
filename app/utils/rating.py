import psycopg

from app.models.videogame_model import get_videogame_by_id


def rate_videogame(conn, uid, vid, score):
    """Insert or update a user's rating for a video game."""
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    
    if int(score) < 0 or int(score) > 5:
        print("Error: Rating must be between 0 and 5 stars.")
        return

    curs = conn.cursor()
    try:
        # Check if the user has already rated the game
        curs.execute("SELECT score FROM user_rates_videogame WHERE uid = %s AND vid = %s", (uid, vid))
        existing_rating = curs.fetchone()

        title = get_videogame_by_id(conn, vid)[0]

        if existing_rating:
            # Update existing rating
            curs.execute("UPDATE user_rates_videogame SET score = %s WHERE uid = %s AND vid = %s", (score, uid, vid))
            print(f"Updated rating for game \"{title}\" to {score}.")
        else:
            # Insert new rating
            curs.execute("INSERT INTO user_rates_videogame (uid, vid, score) VALUES (%s, %s, %s)", (uid, vid, score))
            print(f"Added rating {score} for game \"{title}\".")
        
        conn.commit()
    except psycopg.Error as e:
        print(f"Database error: {e}")
    finally:
        curs.close()

def get_user_rating(conn, uid, vid):
    """Retrieve a user's rating for a specific game."""
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")

    curs = conn.cursor()
    try:
        curs.execute("SELECT Score FROM USER_RATES_VIDEOGAME WHERE UID = %s AND VID = %s", (uid, vid))
        rating = curs.fetchone()
        return rating[0] if rating else None
    except psycopg.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        curs.close()

def get_average_rating(conn, vid):
    """Retrieve the average rating of a video game."""
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")

    curs = conn.cursor()
    try:
        curs.execute("SELECT AVG(Score) FROM USER_RATES_VIDEOGAME WHERE VID = %s", (vid,))
        avg_rating = curs.fetchone()
        return round(avg_rating[0], 2) if avg_rating[0] is not None else None
    except psycopg.Error as e:
        print(f"Database error: {e}")
        return None
    finally:
        curs.close()

def remove_rating(conn, uid, vid):
    """Remove a user's rating for a game."""
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")

    curs = conn.cursor()
    try:
        curs.execute("DELETE FROM USER_RATES_VIDEOGAME WHERE UID = %s AND VID = %s", (uid, vid))
        if curs.rowcount > 0:
            print(f"Removed rating for game {vid}.")
        else:
            print("No rating found to delete.")
        conn.commit()
    except psycopg.Error as e:
        print(f"Database error: {e}")
    finally:
        curs.close()
