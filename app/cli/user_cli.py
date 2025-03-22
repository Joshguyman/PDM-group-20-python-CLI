# Imports
from app.services.user_services import *
import getpass

# Session variables
session_username: str
session_password: str
session_uid: str

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
          "\tRename a Collention (CR)\n"
          "Games:\n"
          "\tPlay a specific Game (PG)\n"
          "\tPlay a random Game from a Collection\n"
          "\tSearch for Game by various ways (SG)\n"
          "\tDelete Games from your Collection (CDG)\n"
          "\tModify the name of one of your Collections (CM)\n"
          "\tDelete one of your Collections (CD)\n"
          "Games:\n"
          "\tPlay a specific Game (PG)\n"
          "\tPlay a random Game from a Collection (PRG)\n"
          "\tSearch for Game by Name (SN)\n"
          "\tSearch for Game by Platform (SPL)\n"
          "\tSearch for Game by Release Date (SR)\n"
          "\tSearch for Game by Developer (SD)\n"
          "\tSearch for Game by Publisher (SPB)\n"
          "\tSearch for Game by Price (SPR)\n"
          "\tSearch for Game by Genre (SG)\n"
          "\tRate a Game (GR)\n"
          "Users:\n"
          "\tSearch for User (SU)\n"
          "\tFollow User (UF)\n"
          "\tUnfollow User (UUF)\n"
          "Rate a Game (R)\n"
          "Quit program (Q)"
    )

def command_handler(conn):
    global session_live

    user_input = input("Enter your command: ").lower()
    match user_input:
        case "h":
            help_message()
        case "cc":
            new_collection(conn, input("Enter a name for your new collection: "), session_uid)
        case "cv":
            get_collection_details(conn, session_uid)
        case "ca":
            added_games_list = []
            adding_games = True
            while (adding_games):
                cur_game = input("Enter the title of the game you with to add: ")
                added_games_list.append(cur_game)
                adding_games = False if (input("Done adding games?(Y/N): ").lower() == "y") else True
            # TODO
        case "cd":
            removed_games_list = []
            removing_games = True
            while (removing_games):
                cur_game = input("Enter the title of the game you with to remove: ")
                removed_games_list.append(cur_game)
                adding_games = False if (input("Done removing games?(Y/N): ").lower() == "y") else True
            while adding_games:
                cur_game = input("Enter the name of the game you wish to add: ")
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
                cur_game = input("Enter the name of the game you with to remove: ")
                removed_games_list.append(cur_game)
                removing_games = False if (input("Done removing games?(Y/N): ").lower() == "y") else True
            clist = get_collection_by_name(conn, session_uid, input("Enter the name of the collection to delete from: "))
            index = 0
            if len(clist) > 1:
                index = int(same_collection_name(conn, clist)) - 1
            remove_games_from_collection(conn, clist[index][1], session_uid, removed_games_list)
        case "sn":
            searched_game = input("Enter game name: ")
            # TODO: Call function once it is implemented
        case "spl":
            searched_platform = input("Enter platform name: ")
            # TODO: Call function once it is implemented
        case "sr":
            searched_release_date = input("Enter release date: ")
            # TODO: Call function once it is implemented
        case "sd":
            searched_developer = input("Enter developer name: ")
            # TODO: Call function once it is implemented
        case "spb":
            searched_publisher = input("Enter publisher name: ")
            # TODO: Call function once it is implemented
        case "spr":
            searched_price = input("Enter price: ")
            # TODO: Call function once it is implemented
        case "sg":
            is_type_valid = False
            valid_types = ["title", "platform", "release date", "developer", "publisher", "genre", "price"]
            while (not is_type_valid):
                print("When searching for a Game, you can search using one of the following:")
                print("Title, Platform, Release Date, Developer, Publisher, Price, Genre, Age Rating")
                searched_type = input("What do to wish to search by: ").lower()
                if (searched_type in valid_types):
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
        case "q":
            session_live = False
        case "su":
            chosen_type = 1
            type_input = input("Search for user by username or email?(U/E): ").lower()
            chosen_type = 0 if (type_input == "u") else 1
            search_input = input("Search for: ")
            search_user(conn, search_input, chosen_type)
        case "uf":
            followed_user = input("Who do you want to follow: ")
            follow_user(conn, session_uid, followed_user)
        case "uuf":
            unfollowed_user = input("Who do you want to unfollow: ")
            unfollow_user(conn, session_uid, unfollowed_user)
        case "r":
            print("TODO")
        case "gr":

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