import sqlite3


class Database:
    """Responsible for the DB communication."""

    __FILE_NAME = 'database.db'
    __CONNECTION = None
    __CURSOR = None


    def __init__(self):
        """The constructor..."""

        pass


    def connect(self):
        """Connects to the database."""

        self.__CONNECTION = sqlite3.connect(self.__FILE_NAME)
        self.__CURSOR = self.__CONNECTION.cursor()


    def __execute(self, query, arguments=None):
        """Executes a statement."""

        self.__CURSOR.execute(query, arguments)


    def fetch_one(self, query):
        """Fetches one row."""

        self.__execute(query)
        return self.__CURSOR.fetchone()


    def fetch_all(self, query):
        """Fetches multiple rows."""

        self.__execute(query)
        return self.__CURSOR.fetchall()


    def execute(self, query, arguments):
        """Executes and commits a create, insert, or drop statement."""

        self.__execute(query, arguments)
        self.__CONNECTION.commit()


    def close(self):
        """Closes the database connection."""

        self.__CONNECTION.close()
        self.__CONNECTION = None
        self.__CURSOR = None
