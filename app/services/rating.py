import psycopg

def rate_videogame(conn, uid, vid, score):
    """Insert or update a user's rating for a video game."""
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    
    if score < 0 or score > 10:
        print("Error: Rating must be between 0 and 10.")
        return

    curs = conn.cursor()
    try:
        # Check if the user has already rated the game
        curs.execute("SELECT Score FROM USER_RATES_VIDEOGAME WHERE UID = %s AND VID = %s", (uid, vid))
        existing_rating = curs.fetchone()

        if existing_rating:
            # Update existing rating
            curs.execute("UPDATE USER_RATES_VIDEOGAME SET Score = %s WHERE UID = %s AND VID = %s", (score, uid, vid))
            print(f"Updated rating for game {vid} to {score}.")
        else:
            # Insert new rating
            curs.execute("INSERT INTO USER_RATES_VIDEOGAME (UID, VID, Score) VALUES (%s, %s, %s)", (uid, vid, score))
            print(f"Added rating {score} for game {vid}.")
        
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
