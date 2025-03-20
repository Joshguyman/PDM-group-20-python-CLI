import psycopg
from sshtunnel import SSHTunnelForwarder

# Constants for connection
DBNAME = "p32001_20"
SSHURL = 'starbug.cs.rit.edu'
SSHPORT = 22
HOSTADDRESS = '127.0.0.1'
HOSTPORT = 5432

"""
connect: sets up db connection and ssh tunnel
@param: username -> database username (i.e abc1234)
@param: password -> your password
returns: psycopg connection on success, none on failure
"""
def connect(username: str, password: str, server):
    params = {
        'dbname': DBNAME,
        'user': username,
        'password': password,
        'host': HOSTADDRESS,
        'port': server.local_bind_port
    }

    conn = psycopg.connect(**params)
    print("Database connection established")
    return conn
"""
close_connection:
@param: conn -> psycopg database connection 
"""
def close_connection(conn: psycopg.Connection):
    print("Attempting to close connection...")
    conn.close()
    print("Connection closed Successfully")
