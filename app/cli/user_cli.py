# Imports
import re

from app.services.user_services import *
from app.models.videogame_model import *
from app.utils.user_follow_util import *
import getpass
from datetime import datetime
# Session variables
session_username: str
session_password: str
session_uid: str
session_time: datetime
session_live: bool = True
credentials_loaded: bool = False

def help_message():
    # TODO: Option to quit loop/program
    print(
          "Display Help message (H)\n"
          "Collections:\n"
          "\tCreate a Collection (CC)\n"
          "\tView Your Collections (CV)\n"
          "\tAdd Games to your Collection (CA)\n"
          "\tDelete Games from your Collection (CD)\n"
          "\tRename a Collection (CR)\n"
          "\tDelete one of your Collections (CRC)\n"
          "Games:\n"
          "\tSearch for Game by various ways (SG)\n"
          "\tPlay a specific Game (PG)\n"
          "\tPlay a random Game from a Collection (PRG)\n"
          "\tStop playing a running Game (PS)\n"
          "\tRate a Game (R)\n"
          "\tTop 20 Video Games in the last 90 days (T20)\n"
          "\tTop N Video Games by various ways (T <N>)\n"
          "\tTop 5 rated releases of the Month (TM)\n"
          "\tRecommend N games by various ways (RG)\n"
          "Users:\n"
          "\tSearch for User (SU)\n"
          "\tFollow User (UF)\n"
          "\tUnfollow User (UUF)\n"
          "\tView number of Users followed (NFD)\n"
          "\tView number of followers (NFS)\n"
          "\tView number of Collections a User has (VNC)\n"
          "\tView the top 20 Games your Followers love! (VTT)\n"
          "Quit program (Q)"
    )

def command_handler(conn):
    global session_live
    global session_time
    user_input = input("Enter your command: ").lower().split(" ")
    match user_input[0]:
        case "h":
            help_message()
        # COLLECTIONS 
        case "cr":
            name = input("Enter the collection you wish to modify: ")
            clist = get_collection_by_name(conn, session_uid, name)
            index = 0
            if len(clist) > 1:
                index = int(same_collection_name(conn, clist)) - 1

            modify_collection_name(conn, session_uid, clist[index][1], input("Enter the name you wish to change it to: "))
        case "cc":
            new_collection(conn, input("Enter a name for your new collection: "), session_uid)
        case "cv":
            get_user_collections(conn, session_uid)
        case "ca":
            added_games_list = []
            adding_games = True
            while adding_games:
                cur_game = input("Enter the title of the game you with to add: ")
                added_games_list.append(cur_game)
                adding_games = False if (input("Done adding games?(Y/N): ").lower() == "y") else True
            clist = get_collection_by_name(conn, session_uid, input("Enter the name of the collection to add to: "))
            index = 0
            if len(clist) > 1:
                index = int(same_collection_name(conn, clist)) - 1
            add_games_to_collection(conn, clist[index][1], session_uid, added_games_list)
        case "cd":
            removed_games_list = []
            removing_games = True
            while removing_games:
                cur_game = input("Enter the title of the game you wish to remove: ")
                removed_games_list.append(cur_game)
                removing_games = False if (input("Done removing games?(Y/N): ").lower() == "y") else True
            clist = get_collection_by_name(conn, session_uid, input("Enter the name of the collection to remove from: "))
            index = 0
            if len(clist) > 1:
                index = int(same_collection_name(conn, clist)) - 1
            remove_games_from_collection(conn, clist[index][1], session_uid, removed_games_list)

        # VIDEO GAMES 
        case "sg":
            is_type_valid = False
            valid_types = ["title", "platform", "release date", "developer", "publisher", "genre", "price"]
            while not is_type_valid:
                print("When searching for a Game, you can search using one of the following:")
                print("Title, Platform, Release Date, Developer, Publisher, Price, Genre, Age Rating")
                searched_type = input("What do to wish to search by: ").lower()
                if searched_type in valid_types:
                    is_type_valid = True
                else:
                    print("Please enter a valid search type.")
            
            searched_input = input(f"Enter desired {searched_type}: ")
            is_default_order = True if (input("Would you like default sorting?(Y/N): ").lower() == "y") else False
            if (is_default_order is True):
                order_input = ""
                is_ascending = True
            else:
                valid_order_types = ["title", "price", "genre", "release-date"]
                is_order_valid = False
                is_ascending = True
                while (not is_order_valid):
                    print("You are able to sort using one of the following:")
                    print("Title, Price, Genre, release-date")
                    order_input = input("What do you wish to order by: ").lower()
                    if (order_input in valid_order_types):
                        is_order_valid = True
                    else:
                        print("Please enter a valid order type.")
                is_ascending = False if (input("Sort by Ascending or Descending?(A/D): ").lower() == "d") else True
            search_videogame(conn, searched_input, searched_type, order_input, not (is_ascending))
        case "pg":
            session_time = play_videogame(conn, input("Enter the game you wish to play: "), session_uid)[1]
        case "prg":
            clist = get_collection_by_name(conn, session_uid, input("Enter the name of the collection to play a Game from: "))
            index = 0
            if len(clist) > 1:
                index = int(same_collection_name(conn, clist)) - 1
            session_time = play_random_videogame(conn,clist[index][1], session_uid)[1]
        case "ps":
            name = input("Enter the game you wish to stop playing: ")
            vid = search_videogame_title(conn, name)[0]
            stop_playing_videogame(conn, session_uid, name, vid, session_time)
        case "t20":
            get_top_20_popular_games(conn)
        case "q":
            session_live = False
        # USER 
        case "su":
            chosen_type = 1
            type_input = input("Search for user by username or email?(U/E): ").lower()
            chosen_type = 0 if (type_input == "u") else 1
            search_input = input("Search for: ")
            search_user(conn, search_input, chosen_type)
        case "uf":
            followed_user = input("Who do you want to follow?: ")
            follow_user(conn, session_uid, followed_user)
        case "uuf":
            unfollowed_user = input("Who do you want to unfollow?: ")
            unfollow_user(conn, session_uid, unfollowed_user)
        case "nfd":
            following_list = get_following_list(conn, session_uid)
            if following_list is not None:
                following_num = len(following_list)
                if following_num == 1:
                    user_word = 'user'
                else:
                    user_word = 'users'
                print("You are currently following", following_num, user_word)
        case "nfs":
            follower_list = get_follower_list(conn, session_uid)
            if follower_list is not None:
                follower_num = len(follower_list)
                if follower_num == 1:
                    follower_word = 'follower'
                else:
                    follower_word = 'followers'
                print("You currently have", follower_num, follower_word)
        case "r":
            vid = search_videogame_title(conn, input("Enter the game you wish to rate: "))[0]
            create_rating(conn, session_uid, vid, input("Enter your score: "))
        case "t":
            if len(user_input) > 1:
                n = int(user_input[1])
            else:
                n = 10 #defualt val
            criteria = input(f"View top {n} video games by rating, playtime, or both (R/P/B): ").upper()
            get_top_n_videogames(conn, criteria, uid=session_uid, n=n)
        case "tm":
            if input("Would you like to view games for a specific(S) or current(C) month?")[0].lower() == "s":
                res = input("Enter the month and year you wish to view (<month>, YYYY): ")
                while not re.match(r'^[A-Z][a-z]{2}, \d{4}$', res):
                    res = input("Incorrect format, Enter <month>, YYYY: ")
                get_top_5_games_of_the_month(conn, res)
            else:
                get_top_5_games_of_the_month(conn, None)
        case "rg":
            res = input("Would you like recommendations based on (G)enre, (D)eveloper, (P)latform, (R)ating, or (S)imilar users?")
            while res[0].upper() != "G" and res[0].upper() != "D" and res[0].upper() != "P" and res[0].upper() != "R" and res[0].upper() != "S":
                res = input("Invalid criteria, Enter G/D/P/R/S: ")
            num = input("Enter the number of recommendations you want: ")
            while not num.isdigit():
                num = input("Please enter a number: ")
            num = int(num)
            recommend_games(conn, session_uid, res, num)
        # DELETE COLLECTION 
        case "crc":
            name = input("Enter the collection you wish to delete: ")
            clist = get_collection_by_name(conn, session_uid, name)
            index = 0
            if len(clist) > 1:
                index = int(same_collection_name(conn, clist)) - 1
            delete_collection(conn, session_uid, clist[index][1])
        case "vnc":
            name = input("Enter the user you wish to check: ")
            uid = get_user_by_username(conn, name)[0]
            count = user_collection_count(conn, uid)
            print(name, "has", count, "collections.")
        case "vtt":
            if not get_follower_list(conn, session_uid):
                print("You're not following anyone :(")
                return
            top20 = top_games_followers(conn, session_uid, 20)
            if not top20:
                return
            print("The top 20 games are...")
            for game in top20:
                print(f"\t{game[1]} of your followers played {game[0]}")

        case _:
            print("Please enter a valid command, input H for help.")
            

def session_loop(conn):
    global session_live
    global credentials_loaded
    global session_username
    global session_password
    global session_uid

    # Pre-loop login/signup
    while (not credentials_loaded):
        login_decision = input("Log in or Sign up (L/S): ")
        if (login_decision.lower() == "l"):
            session_username = input("Enter username: ")
            session_password = getpass.getpass("Enter password: ")
            session_password_confirmation = getpass.getpass("Confirm password: ")

            if (session_password == session_password_confirmation):
                session_uid = sign_in(conn, session_username, session_password)
                if (session_uid):
                    credentials_loaded = True
                # TODO: set credentials_loaded to true under the condition that sign_in worked then proceed to live loop
            else:
                print("Passwords did not match!")

        elif (login_decision.lower() == "s"):
            session_username = input("Enter username: ")
            session_password = getpass.getpass("Enter password: ")
            session_password_confirmation = getpass.getpass("Confirm password: ")
            session_f_name = input("Enter first name: ")
            session_l_name = input("Enter last name: ")
            session_email = input("Enter email: ")
            if (session_password == session_password_confirmation):
                session_uid = create_account(conn, session_username, session_password, session_f_name, session_l_name, session_email)
            else:
                print("Passwords did not match!")

    # Session live loop
    # TODO: Better welcome and leaving message
    print("\n\nWelcome to the videogame program\n")
    help_message()
    while session_live:
        command_handler(conn)
    print("Bye for now")

def same_collection_name(conn, result):
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")

    print(f"{'Entry Name':<15} {'ID':<5}")
    print("-" * 22)
    for name, colid in result:
        print(f"{name:<15} {colid:<5}")
    return input("Which collection were you referring to? (1-n): ")

# mZ1_Rey\
# eharCollection1