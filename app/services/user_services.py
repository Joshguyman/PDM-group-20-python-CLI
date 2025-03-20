
"""
sign_in: sign in with a username and password
@:param username
@:param password
@:return uid of the user
"""
def sign_in(username, password):
    return None
"""
create_account: create an account for a user
@:param username
@:param password
@:param first_name
@:param last_name
@:param email
@:return uid of the created user
"""
def create_account(username, password, first_name, last_name, email):
    return None
"""
new_collection: create a new collection
@:param name -> name of the new collection
@:param uid -> id of the user creating the collection
@:return colid of the new collection
"""
def new_collection(name, uid):
    return None
"""
add_games_to_collection: add games to an existing collection owned by the user
@:param name -> name of the existing collection
@:param uid -> id of the user who owns the collection
@:param games -> list of game titles to add to the collection
@:return None (might change idk)
"""
def add_games_to_collection(name, uid, games:list):
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
search_videogame: search a video game by title, platform, release date, developer, price, genre
@:param val -> the value to be searched
@:param searchtype -> int specifying the search type (i.e 1 for title, 2 for platform, 3 for release date, 4 for developer, 5 for genre)
@:return list of videogames with the specified value
"""
def search_videogame(val, searchtype):
    return None
"""
play_videogame: start playing a video game
@:param name -> the name of the game to be played
@:return tuple containing the vid of the game being played, and the start time of playing the game
"""
def play_videogame(name):
    return None
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
def play_random_videogame(name):
    return None
"""
follow_user: follow a user, updates the corresponding db table for the current user to follow another user
@:param username: the username of the user to be followed
@:return None (idk)
"""
def follow_user(username):
    return None
"""
search_user: searches and returns a uid from the db
@:param val -> the value to be searched
@:param searchtype -> int specifying the search type (i.e 1 for username, 2 for uid, 3 for email)
"""
def search_user(val, searchtype):
    return None