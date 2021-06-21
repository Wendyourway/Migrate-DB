import os
import subprocess
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import connect, Error

database_exception = [
    "information_schema",
    "performance_schema",
    "phpmyadmin",
    "mysql",
    "sys"
]

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

def connect_database():
    host = os.getenv('DB1_HOST')
    user = os.getenv('DB1_USER')
    password = os.getenv('DB1_PASSWORD')
    connection = connect(host,user, password)
    return connection

def get_databases(connection):
    databases = []
    source_cursor = connection.cursor()
    source_cursor.execute("SHOW DATABASES")
    result = source_cursor.fetchall()
    for x in result:
        if x[0] not in database_exception:
            databases.append(x[0])
    return databases

def export_database(database):
    host = os.getenv('DB1_HOST')
    user = os.getenv('DB1_USER')
    password = os.getenv('DB1_PASSWORD')
    command = "mysqldump -h " + host + " -u " + user + " -p" + password + " --databases " + database + " > exports/" + database + ".sql"
    subprocess.run(command, shell=True, check=True, text=True)

def import_database(database):
    host = os.getenv('DB2_HOST')
    user = os.getenv('DB2_USER')
    password = os.getenv('DB2_PASSWORD')
    command = "mysql -h " + host + " -u " + user + " -p" + password + " " + database + " < exports/" + database + ".sql"
    subprocess.run(command, shell=True, check=True, text=True)
    
if __name__ == '__main__':
    load_dotenv()
    source_db = connect_database()
    databases = get_databases(source_db)
    for database in databases:
        try:
            export_database(database)
            import_database(database)
        except:
            print("An exception occurred")