
"""
sign_in: sign in with a username and password
@:param username
@:param password
@:return uid of the user
"""
from app.models.collection_model import *
from app.models.user_model import *
from app.models.videogame_model import *
from app.utils.format import format_videogame_result
from datetime import datetime

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
def add_games_to_collection(conn, colid, uid, games:list):
    collection = get_collection_by_id(conn, colid)
    if check_collection_owner(conn, uid, colid):
        for game in games:
            vid = get_videogame_id(conn, game)
            if vid is None:
                print(f"No such game \"{game}\"")
                continue
            vid = vid[0]
            if check_game_in_collection(conn, colid, vid):
                print(f"\"{game}\" is already in collection \"{collection}\"")
                continue
            add_game(conn, colid, vid)
            print(f"Successfully added \"{game}\" to collection \"{collection}\"")
        contents = get_games_in_collection(conn, colid)
        print(f"Collection \"{collection}\" now contains {contents}")
        return
    print(f"User does not own collection \"{collection}\"")
    return
"""
remove_games_from_collection: remove games from an existing collection owned by the user
@:param name -> name of the existing collection
@:param uid -> id of the user who owns the collection
@:param games -> list of game titles to remove from the collection
@:return None (might change idk)
"""
def remove_games_from_collection(conn, colid, uid, games:list):
    collection = get_collection_by_id(conn, colid)
    if check_collection_owner(conn, uid, colid):
        for game in games:
            vid = get_videogame_id(conn, game)
            if vid is None:
                print(f"No such game \"{game}\"")
                continue
            vid = vid[0]
            if not check_game_in_collection(conn, colid, vid):
                print(f"\"{game}\" is not in collection \"{collection}\"")
                continue
            remove_game(conn, colid, vid)
            print(f"Successfully removed \"{game}\" from collection \"{collection}\"")
        contents = get_games_in_collection(conn, colid)
        print(f"Collection \"{collection}\" now contains {contents}")
        return
    print(f"User does not own collection \"{collection}\"")
    return
"""
search_videogame: search a video game by title, platform, release date, developer, price, genre
@:param val -> the value to be searched
@:param searchtype -> int specifying the search type (i.e 1 for title, 2 for platform, 3 for release date, 4 for developer, 5 for genre)
@:return list of videogames with the specified value
"""
def search_videogame(conn, val, searchtype):
    result = []
    st = str
    match searchtype:
        case "title":
            result = get_videogame_by_title(conn, val)
            st = "Title"
        case "platform":
            result = get_videogame_by_platform(conn, val)
            st = "Platform"
        case "release date":
            result = get_videogame_by_release_date(conn, val)
            st = "Release Date"
        case "developer":
            result = get_videogame_by_dev_name(conn, val)
            st = "Developer"
        case "publisher":
            result = get_videogame_by_pub_name(conn, val)
            st = "Publisher"
        case "genre":
            result = get_videogame_by_genre_name(conn, val)
            st = "Genre"
        case "price":
            result = get_videogame_by_price(conn, val)
            st = "Price"
        case _:
            print("Unrecognized search type")
    format_videogame_result(result,val, st)

"""
play_videogame: start playing a video game
@:param name -> the name of the game to be played
@:return tuple containing the vid of the game being played, and the start time of playing the game
"""
def play_videogame(conn, name, uid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")

    result = search_videogame(conn, name, uid)
    if result:
        curs = conn.cursor()
        vid = result[0]
        try:
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")
            curs.execute(
                "INSERT INTO user_plays_game (uid, vid, timestarted, durationplayed) VALUES (%s, %s, %s, %s)",
                (uid, vid, formatted_time, 0)
            )
            conn.commit()
            curs.close()
            return

        except psycopg.Error as e:
            print(f"Database error: {e}")
            curs.close()
            return None
    else:
        print("Game ID/Username")
        return

"""
stop_playing_videogame: stop playing the currently active video game
updates the database with the elapsed time since starting the game
@param name -> the name of the game to be stopped
"""
def stop_playing_videogame(name):
    return None

"""
play_videogame: start playing a random video game from a collection
@:param name -> the name of the collection
@:return tuple containing the vid of the game being played, and the start time of playing the game
"""
def play_random_videogame(conn, collection):

    return None
"""
follow_user: follow a user, updates the corresponding db table for the current user to follow another user
@:param followee: id of user that wants to follow
@:param username: the username of the user to be followed
@:return None (idk)
"""
def follow_user(conn, followee, username):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")

    result = get_user_by_username(conn, username)
    if result and get_user_by_id(conn, followee):
        curs = conn.cursor()
        follower = result[0]
        try:
            curs.execute(
                "INSERT INTO user_follows_user (follower, followee) VALUES (%s, %s)",
                (followee, follower)
            )
            conn.commit()
            curs.close()
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
