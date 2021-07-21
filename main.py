import os
import time
import subprocess
import getpass
import calendar
import mysql.connector
import pyfiglet
from mysql.connector import connect, Error
from decouple import config


database_exception = [
    "information_schema",
    "performance_schema",
    "phpmyadmin",
    "mysql",
    "sys"
]

timestamp = calendar.timegm(time.gmtime())

source_connection = None
destination_connection = None

sourceHost = config("source_host")
sourceUser = config("source_user")
sourcePass = config("source_pass")
databases = config("databases")
drop_database = config("drop_database")
destinationHost = config("destination_host")
destinationUser = config("destination_user")
destinationPass = config("destination_pass")

"""Connect
: param host: the hostname to export from
: type host: str
: param username: the username to use
: type username: str
: param password: the password to use
: type password: str
"""


def connect(host, username, password):
    """ Connect to MySQL database """
    conn = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        auth_plugin='mysql_native_password'
    )
    if conn.is_connected():
        print('Connected to MySQL database')
        return conn


def get_databases(connection):
    databases = []
    source_cursor = connection.cursor()
    source_cursor.execute("SHOW DATABASES")
    result = source_cursor.fetchall()
    for x in result:
        if x[0].decode() not in database_exception:
            databases.append(x[0].decode())
    return databases


"""Exports the database
:param hostname: the hostname to export from
:type hostname: str
:param username: the username to use
:type username: str
:param password: the password to use
:type password: str
:param database: the database to export
:type database: str
:returns: Nothing
"""


def export_db(hostname, username, password, database):

    command = "mysqldump -h " + hostname + " -u " + username + " -p" + password + \
        " --databases " + database + " --no-create-db > exports/" + \
        str(timestamp) + "-" + database + ".sql"
    subprocess.run(command, shell=True, check=True, text=True)


"""Imports the database

:param hostname: the hostname to export from
:type hostname: str
:param username: the username to use
:type username: str
:param password: the password to use
:type password: str
:param database: the database to export
:type database: str
:returns: Nothing
"""


def import_db(hostname, username, password, database):
    if(drop_database):
        command = "mysql -h " + str(hostname) + " -u " + str(username) + \
            " -p" + str(password) + " -e \"DROP DATABASE IF EXISTS " + \
            str(database) + "\""
        subprocess.run(command, shell=True, check=True, text=True)
    command = "mysql -h " + str(hostname) + " -u " + str(username) + \
        " -p" + str(password) + " -e \"CREATE DATABASE " + str(database) + "\""
    subprocess.run(command, shell=True, check=True, text=True)
    command = "mysql -h " + str(hostname) + " -u " + str(username) + " -p" + str(password) + \
        " " + str(database) + " < exports/" + str(timestamp) + \
        "-" + str(database) + ".sql"
    subprocess.run(command, shell=True, check=True, text=True)


if __name__ == '__main__':
    ascii_banner = pyfiglet.figlet_format("DATABASE MIGRATION")
    print(ascii_banner)
    if (not sourceHost):  # is source empty?
        # get source host from input
        sourceHost = input("Enter Source Host: ")

    if(not sourceUser):
        sourceUser = input("Enter Source Username: ")
    if (not sourcePass):
        sourcePass = getpass.getpass(prompt='Enter Source Password: ')
    # remove white spaces
    databases.replace(" ", "")

    source_connection = connect(sourceHost, sourceUser, sourcePass)
    if(source_connection):
        print("Source connected...")
        if(not databases):
            # No detabase specified, so we get all of them.
            databases = get_databases(source_connection)
        else:
            databases = databases.split(",")
        if (not destinationHost):
            destinationHost = input("Enter Destination Host: ")
        if (not destinationUser):
            destinationUser = input("Enter Destination Username: ")
        if (not destinationPass):
            destinationPass = getpass.getpass(
                prompt='Enter Destination Password: ')
        destination_connection = connect(
            destinationHost, destinationUser, destinationPass)
        for database in databases:
            export_db(sourceHost, sourceUser, sourcePass, database)
            if destination_connection is not False:
                import_db(destinationHost, destinationUser,
                          destinationPass, database)
                print(database + ": import successful")
            else:
                print("not importing")
    else:
        print("Failed to connect to source host")
