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

