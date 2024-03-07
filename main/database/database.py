import os
import sqlite3
from pathlib import Path


class Database:
    """Responsible for the DB communication."""

    __FILE_NAME = Path(os.path.dirname(os.path.abspath(__file__))) / 'database.db'
    __CONNECTION = None
    __CURSOR = None


    def connect(self):
        """Connects to the database."""

        self.__CONNECTION = sqlite3.connect(self.__FILE_NAME)
        self.__CURSOR = self.__CONNECTION.cursor()


    def __execute(self, query, arguments=None):
        """Executes a statement."""

        if arguments != None:
            self.__CURSOR.execute(query, arguments)
            return
        self.__CURSOR.execute(query)


    def fetch_one(self, query, arguments=None):
        """Fetches one row."""

        self.__execute(query, arguments)
        return self.__CURSOR.fetchone()


    def fetch_all(self, query, arguments=None):
        """Fetches multiple rows."""

        self.__execute(query, arguments)
        return self.__CURSOR.fetchall()


    def execute(self, query, arguments=None):
        """Executes and commits a create, insert, or drop statement."""

        self.__execute(query, arguments)
        self.__CONNECTION.commit()


    def last_row_id(self):
        """Fetches the last generated ID."""

        return self.__CURSOR.lastrowid


    def close(self):
        """Closes the database connection."""

        self.__CONNECTION.close()
        self.__CONNECTION = None
        self.__CURSOR = None
