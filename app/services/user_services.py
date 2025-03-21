
"""
sign_in: sign in with a username and password
@:param username
@:param password
@:return uid of the user
"""
from app.models.user_model import *
from app.models.videogame_model import *
from datetime import datetime
from app.models.collection_model import *
import random


def sign_in(conn, username, password):
    result = get_user_by_username(conn, username)
    if not result:
        print("User not found")
        return None
    tmp = get_user_password(conn, result[0])[0]
    if password != tmp :
        print(f"No User with password \"{password}\"")
        return None
    print("Signed in as:", result[1])
    return result[0]
"""
create_account: create an account for a user
@:param username
@:param password
@:param first_name
@:param last_name
@:param email
@:return uid of the created user
"""
def create_account(conn, username, password, first_name, last_name, email):
    result = create_user(conn, username, password, first_name, last_name, email)
    if not result:
        print(f"Username \"{username}\" or Email \"{email}\" is already in use")
        return None

    print("Successfully created account")
    return result[0]

"""
new_collection: create a new collection
@:param name -> name of the new collection
@:param uid -> id of the user creating the collection
@:return colid of the new collection
"""
def new_collection(conn, name, uid):
    colid = create_collection(conn, name, uid)
    if not colid:
        print("Issue creating collection")
        return None
    print(f"Successfully created \"{name}\" collection")
    return colid
"""
add_games_to_collection: add games to an existing collection owned by the user
@:param colid -> id of the existing collection
@:param uid -> id of the user who owns the collection
@:param games -> list of game titles to add to the collection
@:return None (might change idk)
"""
def add_games_to_collection(colid, uid, games:list):
    return None
"""
remove_games_from_collection: remove games from an existing collection owned by the user
@:param name -> name of the existing collection
@:param uid -> id of the user who owns the collection
@:param games -> list of game titles to remove from the collection
@:return None (might change idk)
"""
def remove_games_from_collection(colid, uid, games:list):
    return None
"""
search_videogame: search videogame by title, returns vid, helper function for play_videogame
@:param conn -> connection
@:param title -> name of game to search
@:return vid of given game
"""
def search_videogame(conn, title):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")

    curs = conn.cursor()
    try:
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
play_videogame: start playing a video game
@:param conn -> connection
@:param name -> the name of the game to be played
@:param uid -> id of user asking to play
@:return tuple containing the vid of the game being played, and the start time of playing the game
"""
def play_videogame(conn, name, uid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")

    result = search_videogame(conn, name)
    if result:
        curs = conn.cursor()
        vid = result[0]
        try:
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
            curs.execute(
                "INSERT INTO user_plays_videogame (uid, vid, timestarted, durationplayed) VALUES (%s, %s, %s, %s)",
                (uid, vid, formatted_time, "00:00")
            )
            conn.commit()
            curs.close()
            print("Started playing", name)
            return vid, current_time

        except psycopg.Error as e:
            print(f"Database error: {e}")
            curs.close()
            return
    else:
        print("Invalid game name")
        return

"""
stop_playing_videogame: stop playing the currently active video game
updates the database with the elapsed time since starting the game
@param conn -> connection
@param uid -> id of user to stop playing
@param name -> the name of the game to be stopped
@param vid -> id of game to be stopped
@param start_time -> start time of game being stopped
@return -> none
"""
def stop_playing_videogame(conn, uid, name, vid, start_time):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")

    curs = conn.cursor()
    try:
        curs.execute(
            "SELECT uid FROM user_plays_videogame WHERE uid = %s AND vid =%s AND durationplayed = '00:00' AND timestarted = %s", (uid, vid, start_time,))
        test = curs.fetchall()
        if start_time and test:
            end_time = datetime.now()
            time_difference = end_time - start_time
            total_seconds = time_difference.total_seconds()
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            elapsed_time = f"{int(hours):02d}:{int(minutes):02d}"
            print("Played", name, "for", elapsed_time, ".")
            curs.execute(
                "UPDATE user_plays_videogame SET durationplayed = %s WHERE uid = %s AND vid =%s AND durationplayed = '00:00'", (elapsed_time, uid, vid,)
            )
            conn.commit()
            curs.close()
        else:
            print("Given game has already ended/Invalid game")
    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return


"""
play_random_videogame: start playing a random video game from a collection
@:param conn -> connection
@:param colid -> the id of the collection
@:param uid -> the id of the user
@:return tuple containing the vid of the game being played, , user id, and the start time of playing the game
"""
def play_random_videogame(conn, colid, uid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "SELECT name FROM collection WHERE uid = %s AND colid = %s", (uid, colid,))
        test = curs.fetchall()
    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return
    games = get_games_in_collection(conn, colid)
    length = len(games)
    if length > 0 and test:
        rand = random.randint(0, length - 1)
        vid, current = play_videogame(conn, games[rand], uid)
        return vid, current, games[rand]
    else:
        print("Invalid collection")
        curs.close()
        return


"""
follow_user: follow a user, updates the corresponding db table for the current user to follow another user
@:param follower: id of user that wants to follow
@:param username: the username of the user to be followed
@:return None
"""
def follow_user(conn, follower, username):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")

    result = get_user_by_username(conn, username)
    if result and get_user_by_id(conn, follower):
        curs = conn.cursor()
        followee = result[0]
        try:
            curs.execute(
                "INSERT INTO user_follows_user (follower, followee) VALUES (%s, %s)",
                (follower, followee)
            )
            conn.commit()
            curs.close()
            print(username, "followed!")
            return

        except psycopg.Error as e:
            print(f"Database error: {e}")
            curs.close()
            return None
    else:
        print("Invalid ID/Username")
        return


"""
unfollow_user: unfollow a user, updates the corresponding db table for the current user to unfollow another user
@:param follower: id of user that wants to unfollow
@:param username: the username of the user to be unfollowed
@:return None
"""
def unfollow_user(conn, follower, username):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")

    result = get_user_by_username(conn, username)
    if result and get_user_by_id(conn, follower):
        curs = conn.cursor()
        followee = result[0]
        try:
            curs.execute(
                "DELETE FROM user_follows_user WHERE follower = %s AND followee = %s",
                (follower, followee)
            )
            conn.commit()
            curs.close()
            print(username, "unfollowed!")
            return

        except psycopg.Error as e:
            print(f"Database error: {e}")
            curs.close()
            return None
    else:
        print("Invalid ID/Username")
        return


"""
search_user: searches and returns a uid from the db
@:param conn -> connection 
@:param val -> the value to be searched
@:param searchtype -> int specifying the search type (i.e 0 for username, 1 for email)
"""
def search_user(conn, val, searchtype):
    match searchtype:
        case 0:
            result = get_user_by_username(conn, val)
            if result:
                print(result)
                return result[0]
            else:
                print("User not found")
                return
        case 1:
            result = get_user_by_email(conn, val)
            if result:
                print(result)
                return result[0]
            else:
                print("User not found")
                return
        case _:
            print("Incorrect search type")
            return


"""
update_last_access: changes corresponding lastaccess value in users table
@:param conn -> connection
@:param uid -> id of user accessing
@:param access -> access time by user
@:return -> none
"""
def update_last_access(conn, uid, access):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    try:
        curs = conn.cursor()
        curs.execute(
            "UPDATE users SET lastaccess = %s WHERE uid = %s", (access, uid,))
        conn.commit()
        curs.close()
        return

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return


"""
user_accesses_application: inserts access time to user_platform_access, calls update_last_access
@:param conn -> connection
@:param uid -> id of user accessing
@:return -> none
"""
def user_accesses_application(conn, uid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")

    access = datetime.now()
    try:
        curs = conn.cursor()
        curs.execute(
            "INSERT INTO user_platform_access (uid, timeaccessed) VALUES (%s, %s)", (uid, access,))
        conn.commit()
        curs.close()
        update_last_access(conn, uid, access)
        return

    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return


