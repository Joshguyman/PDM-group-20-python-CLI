import getpass
from app.models.db import connect, close_connection
from app.models.user_model import *
from app.models.videogame_model import *
from app.models.collection_model import *
from app.services.user_services import *
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
            test = int(input("Enter a collection ID: "))

            games = get_games_in_collection(conn, test)

            if games:
                print(f"Games in collection {test}: {games}")
            else:
                print(f"No games found in collection {test}")

            close_connection(conn)
    except:
        print("Connection failed")

if __name__ == "__main__":
    main()
