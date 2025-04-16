from app.models.collection_model import *
from app.models.user_model import *
from app.models.videogame_model import *
from app.utils.format import format_videogame_result, format_collection_result, format_videogame_date_results
from app.utils.hashing_util import *
from datetime import datetime
from app.models.collection_model import *
import random

from app.utils.rating import rate_videogame


def sign_in(conn, username, password):
    result = get_user_by_username(conn, username)
    if not result:
        print("User not found")
        return None
    tmp = get_user_password(conn, result[0])[0]
    if not (verify_password(password, tmp)) :
        print(f"No User with password \"{password}\"")
        return None
    print("Signed in as:", result[1])
    update_last_access(conn, result[0], datetime.now())
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
    hashed_password = hash_password(password)
    result = create_user(conn, username, hashed_password, first_name, last_name, email)
    if not result:
        print(f"Username \"{username}\" or Email \"{email}\" is already in use")
        return None
    print("Successfully created account")
    return result


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


def add_games_to_collection(conn, colid, uid, games: list):
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
            game_platforms = get_videogame_platforms(conn, vid)
            has = False
            if(game_platforms):
                for pid in game_platforms:
                    if check_user_platform(conn, uid, pid[0]):
                        has = True
                if not has:
                    print(f"WARNING: You do not own a Platform that \"{game}\" is on")
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


def remove_games_from_collection(conn, colid, uid, games: list):
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
search_videogame: search videogame by title, returns vid, helper function for play_videogame
@:param conn -> connection
@:param title -> name of game to search
@:return vid of given game
"""


def search_videogame(conn, val, searchtype, sorttype, desc: bool):
    result = []
    st = str
    sot = 0

    match sorttype:
        case "rating":
            sot = 9
        case "price":
            sot = 8
        case "genre":
            sot = 6
        case "release-date":
            sot = 7

        case _:
            sot = 0
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
    format_videogame_result(result, val, st, sot, desc)


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

    result = search_videogame_title(conn, name)
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
            "SELECT uid FROM user_plays_videogame WHERE uid = %s AND vid = %s AND durationplayed = '00:00' AND timestarted = %s",
            (uid, vid, start_time,))
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
                "UPDATE user_plays_videogame SET durationplayed = %s WHERE uid = %s AND vid = %s AND durationplayed = '00:00'",
                (elapsed_time, uid, vid,)
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
    print(username)
    result = get_user_by_username(conn, username)
    print(result)
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


def get_user_collections(conn, uid):
    collections = get_collection_details(conn, uid)
    if not collections:
        print("You currently have no collections.")
        return
    print(f"You currently have {len(collections)} collection(s):")
    format_collection_result(collections)
    return

def add_platform(conn, uid, pid):
    pname = get_platform_by_id(conn, pid)
    if not check_user_platform(conn, uid, pid):
        if add_platform(conn, uid, pid):
            print(f"You now own {pname} platform")
            return
        print("Error adding platform")
        return
    print(f"You already own the \"{pname}\"")
    return

def user_accesses_application(conn, uid):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")

    access = datetime.now()
    curs = conn.cursor()
    try:
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

def modify_collection_name(conn, uid, colid, name):
    if not check_collection_owner(conn, uid, colid):
        print("You do not own this collection")
    oldname = get_collection_by_id(conn, colid)
    change_collection_name(conn, uid, colid, name)
    print(f"Successfully renamed \"{oldname}\" Collection to \"{name}\" Collection")


def user_collection_count(conn, uid):
    if not get_user_by_id(conn, uid):
        print("User does not exist")
        return
    count = get_number_collections(conn, uid)
    return count
  
def get_top_n_videogames(conn, criterion='R', uid=None, n:int=10):
    """Retrieve and display the top 10 video games based on the chosen criterion"""
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    
    if not uid:
        raise ValueError("UID must be provided for the logged-in user.")
    
    criterion = criterion.upper()  # Normalize input to uppercase
    
    criteria = {'R', 'P', 'B'}
    if criterion not in criteria:
        raise ValueError(f"Invalid criterion. Choose from {criteria}")
    
    query = ""
    
    if criterion == 'R':
        query = """
            SELECT v.vid, v.title, urv.score
            FROM videogame v
            JOIN user_rates_videogame urv ON v.vid = urv.vid
            WHERE urv.uid = %s
            ORDER BY urv.score DESC
            LIMIT %s;
        """
    
    elif criterion == 'P':
        query = """
            SELECT v.vid, v.title, 
                COALESCE(SUM(
                    (CAST(SPLIT_PART(upv.durationplayed, ':', 1) AS INT) * 60) +
                    CAST(SPLIT_PART(upv.durationplayed, ':', 2) AS INT)
                ), 0) AS total_playtime
            FROM videogame v
            JOIN user_plays_videogame upv ON v.vid = upv.vid
            WHERE upv.uid = %s
            GROUP BY v.vid, v.title
            ORDER BY total_playtime DESC
            LIMIT %s;
        """
    
    elif criterion == 'B':
        query = """
            SELECT v.vid, v.title, 
                   urv.score, 
                   COALESCE(SUM(
                        (CAST(SPLIT_PART(upv.durationplayed, ':', 1) AS INT) * 60) +
                        CAST(SPLIT_PART(upv.durationplayed, ':', 2) AS INT)
                   ), 0) AS total_playtime,
                   (urv.score * 0.7 + COALESCE(SUM(
                        (CAST(SPLIT_PART(upv.durationplayed, ':', 1) AS INT) * 60) +
                        CAST(SPLIT_PART(upv.durationplayed, ':', 2) AS INT)
                   ), 0) * 0.3) AS combined_score
            FROM videogame v
            JOIN user_rates_videogame urv ON v.vid = urv.vid
            LEFT JOIN user_plays_videogame upv ON v.vid = upv.vid AND upv.uid = urv.uid
            WHERE urv.uid = %s
            GROUP BY v.vid, v.title, urv.score
            ORDER BY combined_score DESC
            LIMIT %s;
        """
    with conn.cursor() as curs:
        try:
            curs.execute(query, (uid, n))  # Always filter by UID

            result = curs.fetchall()

            # Display results
            if result:
                i = 0
                if criterion == 'R':
                    print(f"\nTop {n} Video Games by RATING for UID = {uid}:")
                    for idx, game in enumerate(result, start=1):
                        i = idx
                        print(f"{idx}. [RATING: {game[2]}] --- VID: {game[0]} --- {game[1]}")
                    if i < n:
                        for idx in range(i, n + 1):
                            print(f"{idx}. ----------------------------------")
                elif criterion == 'P':
                    print(f"\nTop {n} Video Games by PLAYTIME for UID = {uid}:")
                    for idx, game in enumerate(result, start=1):
                        print(f"{idx}. [PLAYTIME: {game[2]} minutes] --- VID: {game[0]} --- {game[1]}")
                    if i < n:
                        for idx in range(i, n + 1):
                            print(f"{idx}. ----------------------------------")
                elif criterion == 'B':
                    print(f"\nTop {n} Video Games by COMBINED SCORE (Rating + Playtime) for UID = {uid}:")
                    for idx, game in enumerate(result, start=1):
                        print(f"{idx}. [COMBINED SCORE: {game[4]:.2f}] --- VID: {game[0]} --- {game[1]}")
                    if i < n:
                        for idx in range(i, n + 1):
                            print(f"{idx}. ----------------------------------")
            else:
                print(f"No data found for UID = {uid} and selected criterion.")

        except psycopg.Error as e:
            print(f"Database error: {e}")
            return []

def sort_top(games, size):
    return sorted(games.items(), key=lambda x: x[1], reverse=True)[:size]
  
def top_games_followers(conn, uid, size):
    top20 = {}
    followers = get_user_followers(conn, uid)
    for follower in followers:
        games = get_user_videogame_plays(conn, follower)
        if not games:
            continue
        for game in games:
            game_name = get_videogame_by_id(conn, game)[0]
            if game_name in top20:
                top20[game_name] += 1
            else:
                top20[game_name] = 1
    if not top20:
        print("Your followers don't own any games :(")
        return
    return sort_top(top20, size)


def get_top_5_games_of_the_month(conn, month):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")

    date = datetime.now().strftime("%B")[:3] + " " + datetime.now().strftime("%Y")
    if month:
        date = month
    result, curs = get_top_5_games_by_date(conn, date)
    format_videogame_date_results(result, date)
"""
recommend games to a user based on some value
type: the type of recommendation (by genre, developer, platform, rating, similar users)
num: number of recommendations
"""
def recommend_games(conn, uid, type, num):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    vids = []
    rec = type
    match type:
        case "G":
            rec = 'Genre'
            vids = get_similar_games_by_genre(conn, uid, num)
        case "D":
            rec = 'Developer'
            vids = get_similar_games_by_dev(conn, uid, num)
        case "P":
            rec = 'Platform'
            vids = get_similar_games_by_plat(conn, uid, num)
        case "R":
            rec = 'Rating'
            vids = get_similar_games_by_rat(conn, uid, num)
        case "S":
            rec = "Similar users"
            vids = get_similar_user_recs(conn, uid, num)
        case _:
            print(f"No recommendations of type \"{rec}\"")
            return
    if not vids:
        print("No similar games found based on your play history.")
        return
    if len(vids) < num:
        print(f"Only able to recommend {len(vids)} games by {rec} based on your play history:")
    print(f"Top {num} recommended games by {rec}, based on your play history:")
    for vid in vids:
        game = get_videogame_by_id_short(conn, vid[0])
        print("=" * 80)
        print(f"Title: {game[0]}")
        print(f"Platforms: {game[1]}")
        print(f"Publishers: {game[2]}")
        print(f"Developers: {game[3]}")
        print(f"Genres: {game[4]}")
        print(f"ESRB Rating: {game[5]}")
        print(f"Average Score: {round(int(game[6]))}")
        print("=" * 80)



"""
wrapper functions ¯\_(ツ)_/¯
"""
def create_rating(conn, uid, vid, score):
    rate_videogame(conn, uid, vid, score)
def remove_rating(conn, uid, vid):
    remove_rating(conn, uid, vid)
