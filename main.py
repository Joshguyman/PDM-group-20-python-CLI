import psycopg
import getpass
import json
import warnings
from sshtunnel import SSHTunnelForwarder

warnings.simplefilter("ignore", category=getpass.GetPassWarning)

secretfile = open("secret.json")
secret = json.load(secretfile)
secretfile.close

username = secret["username"] if secret["username"] != "FILL"  else input("Enter username: ")
password = secret["password"] if secret["password"] != "FILL" else getpass.getpass("Enter password: ")
dbName = "p32001_20"


try:
    with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                            ssh_username=username,
                            ssh_password=password,
                            remote_bind_address=('127.0.0.1', 5432)) as server:
        server.start()
        print("SSH tunnel established")
        params = {
            'dbname': dbName,
            'user': username,
            'password': password,
            'host': '127.0.0.1',
            'port': server.local_bind_port
        }

        conn = psycopg.connect(**params)
        curs = conn.cursor()
        print("Database connection established")

        #DB work here....
    
        print("Attmepting to close connction...")
        conn.close()
        print("Connection closed")

except Exception as e:
    print("Connection failed", e)
