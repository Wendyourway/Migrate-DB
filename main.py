import os
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error

def connect(host, username, password):
    """ Connect to MySQL database """
    conn = None
    try:
        conn = mysql.connector.connect(host=host, user=username, password=password)
        if conn.is_connected():
            print('Connected to MySQL database')
            return conn
    except Error as e:
        print(e)
    finally:
        if conn is not None and conn.is_connected():
            conn.close()


def connect_source_db():
    host = os.getenv('DB1_HOST')
    user = os.getenv('DB1_USER')
    password = os.getenv('DB1_PASSWORD')
    connection = connect(host,user, password)
    return connection
    
if __name__ == '__main__':
    load_dotenv()
    source_db = connect_source_db()
