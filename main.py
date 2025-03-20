import getpass
from app.models.db import connect, close_connection
from app.models.user_model import *
from app.models.videogame_model import *
from app.models.collection_model import *
from app.services.user_services import *
from app.services.rating import *
from sshtunnel import SSHTunnelForwarder

def main():
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    try:
        print("Attempting to create SSH tunnel...")
        with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                                ssh_username=username,
                                ssh_password=password,
                                remote_bind_address=('127.0.0.1', 5432)) as server:
            print("SSH Tunnel Established")
            server.start()

            print(f"Local bind port: {server.local_bind_port}")
            conn = connect(username=username, password=password, server=server)

            # use this for testing currently
            if not conn:
                print("Failed to connect to the database")
                return
            print("Database connection established successfully!")
            print("Welcome to the Video Game Rating System")

            while True:
                print("\nMenu:")
                print("1. Rate a video game")
                print("2. View your rating for a game")
                print("3. View average rating of a game")
                print("4. Remove your rating")
                print("5. Exit")
                
                choice = input("Enter your choice: ")

                if choice == "1":
                    uid = int(input("Enter your UID: "))
                    vid = int (input("Enter the VID: "))
                    score = int(input("Enter your rating (0-10): "))
                    rate_videogame(conn, uid, vid, score)
                elif choice == "2":
                    uid = int(input("Enter your UID: "))
                    vid = int (input("Enter the VID: "))
                    rating = get_user_rating(conn, uid, vid)
                    if rating is not None:
                        print(f"Your rating for game {vid}: {rating}")
                    else:
                        print("You have not rated this game.")
                elif choice == "3":
                    vid = int (input("Enter the VID: "))
                    avg = get_average_rating(conn, vid)
                    if avg is not None:
                        print(f"Average rating for game {vid}: {avg}")
                    else:
                        print("No ratings found for this game")
                elif choice == "4":
                    uid = int(input("Enter your User ID: "))
                    vid = int(input("Enter the Video Game ID: "))
                    remove_rating(conn, uid, vid)
                elif choice == "5":
                    print("Exiting...")
                    close_connection(conn)
                    break

                else:
                    print("Invalid choice. Please enter a valid option.")

            close_connection(conn)
            print("Connection closed")
    except:
        print("Connection failed")

if __name__ == "__main__":
    main()


