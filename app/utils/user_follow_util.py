"""
user_following_util.py

Extra utility functions to help perform
user following functionality
"""

import psycopg


def get_following_list(conn, follower_id):
    """
    Get a user's following list
    :param conn: Data base connection
    :param follower_id: User's ID
    :return: List of user's followers, empty if 0, None if error.
    """
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "SELECT followee from user_follows_user WHERE follower = %s", (follower_id,)
        )
        following = [row[0] for row in curs.fetchall()]

        if not following:
            return []

        return following
    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None


def get_follower_list(conn, followee_id):
    """
    Get a user's follower list
    :param conn: Data base connection
    :param followee_id: User's ID
    :return: List of user's followers, empty if 0, None if error.
    """
    if not conn:
        raise psycopg.OperationalError("Database connection is not established")
    curs = conn.cursor()
    try:
        curs.execute(
            "SELECT follower from user_follows_user WHERE followee = %s", (followee_id,)
        )
        followers = [row[0] for row in curs.fetchall()]

        if not followers:
            return []

        return followers
    except psycopg.Error as e:
        print(f"Database error: {e}")
        curs.close()
        return None
