# Imports
from app.services.user_services import *
import getpass


# Session variables
session_username: str
session_password: str

credentials_loaded: bool = False

def session_loop():
    global credentials_loaded
    # Pre-loop login/signup
    while (not credentials_loaded):
        login_decision = input("Log in or Sign up (L/S): ")
        if (login_decision.lower() == "l"):
            session_username = input("Enter username: ")
            session_password = getpass.getpass("Enter password: ")
            session_password_confirmation = getpass.getpass("Confirm password: ")

            if (session_password == session_password_confirmation):
                print("passwords match")
                sign_in(session_username, session_password)
                # TODO: set credentials_loaded to true under the condition that sign_in worked then proceed to live loop
            else:
                print("Passwords did not match!")

        elif (login_decision.lower() == "s"):
            session_username = input("Enter username: ")
            session_password = getpass.getpass("Enter password: ")
            session_password_confirmation = getpass.getpass("Confirm password: ")
            session_f_name = input("Enter first name: ")
            session_l_name = input("Enter last name")
            session_email = input("Enter email: ")
            if (session_password == session_password_confirmation):
                print("passwords match")
                # create_account(session_username, session_password, session_f_name, session_l_name, session_email)
                # TODO: bring back to start of loop (should already happen) on the condition there was not already-
                # - a present username or email (this should happen in utls folder or model folder)
            else:
                print("Passwords did not match!")


    # Session live loop
