import os.path
import sqlite3
from datetime import datetime


class DataBase:
    def __init__(self):
        self.db_name = "database.db"
        self.setup_db()

    def check_file(self):
        # Check for db
        return os.path.isfile(self.db_name)

    def setup_db(self):
        # If file doesn't exist make table
        if not self.check_file():
            self.connect_db()
            self.create_table()

    def connect_db(self):
        # Connect to database
        return sqlite3.connect(self.db_name)

    def create_table(self):
        sql_command = """
            CREATE TABLE users (
            message_number INTEGER PRIMARY KEY,
            username VARCHAR(64),
            password VARCHAR(64));"""
        self.write_db(sql_command)

    def write_db(self, command, *value):
        # Write raw command
        connection = self.connect_db()
        cursor = connection.cursor()
        cursor.execute(command, *value)
        connection.commit()

    def write(self, username, password):
        # Write data as message
        sql_command = """INSERT INTO users
        (message_number, username, password)
        VALUES (NULL, ?, ?);"""
        self.write_db(sql_command, (username, password))

    def read_db(self, command, *value):
        # Read raw command
        connection = self.connect_db()
        cursor = connection.cursor()
        cursor.execute(command, *value)
        result = cursor.fetchall()
        return result

    def read_all(self):
        # Read all messages
        data = "SELECT * FROM users"
        return self.read_db(data)
