import base64
import bcrypt


def hash_password(password: str) -> str:
    """
    Generate a salted and hashed password using bcrypt and return it as a Base64-encoded string.

    :param password: The raw password of a user.
    :return: A Base64-encoded hashed password (as a string).
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return base64.b64encode(hashed_password).decode()  # Convert bytes to Base64 string


def verify_password(raw_password: str, hashed_password: str) -> bool:
    """
    Verify if the input password matches the stored hashed password.

    :param raw_password: The raw password given by a user.
    :param hashed_password_str: The Base64-encoded hashed password stored in the database.
    :return: True if the passwords match, False otherwise.
    """
    hashed_password_bytes = base64.b64decode(hashed_password)  # Decode Base64 to bytes
    return bcrypt.checkpw(raw_password.encode(), hashed_password_bytes)
