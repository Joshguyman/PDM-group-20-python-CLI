"""
This Module provides functionality to establish an SSH tunnel, connect to a remote
database through the tunnel and execute a session loop for user interaction
with the database.

Authors:
Team 20
    Y. Arden
    S. Le
    J. Espejo
    J. Elliot
    C. Clerigo
"""

import getpass
from app.cli.user_cli import *
from app.models.db import connect, close_connection
from app.models.collection_model import *
from sshtunnel import SSHTunnelForwarder
import time
import json


def main():
    """
    Main function to estalish an SSH tunnel, connect to a remote database, and initiate a session
    loop for user interaction.
    """
    # Secret loading section
    file_path = "secret.json"
    secret = ""
    try:
        with open(file_path, 'r') as file:
            secret = json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}")
        print("Please follow the instructions in \'secret_TEMPLATE.json\'")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in: {file_path}")
        return None
    except Exception as e:
         print(f"An unexpected error occurred: {e}")
         return None

    # Credentials input section
    username = secret["username"] if (secret["username"] != "FILL") else input("Username: ")
    password = secret["password"] if (secret["password"] != "FILL") else getpass.getpass("Password: ")
    
    # Establish connections
    try:
        #print("Attempting to create SSH tunnel...")
        with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                                ssh_username=username,
                                ssh_password=password,
                                remote_bind_address=('127.0.0.1', 5432)) as server:
            #print("SSH Tunnel Established")
            server.start()

            #print(f"Local bind port: {server.local_bind_port}")
            conn = connect(username=username, password=password, server=server)

            # use this for testing currently
            session_loop(conn)
            # Get user ID

            close_connection(conn)
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    main()
