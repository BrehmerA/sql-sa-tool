import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Appends the parent dir to the python path.

from main.database.database import Database


class DatabaseTest(unittest.TestCase):


    def test_connect(self):
        db = Database()
        db.connect()
        self.assertIsNotNone(db._Database__CONNECTION)
        self.assertIsNotNone(db._Database__CURSOR)


    def test_close(self):
        db = Database()
        db.connect()
        db.close()
        self.assertIsNone(db._Database__CONNECTION)
        self.assertIsNone(db._Database__CURSOR)


if __name__ == '__main__':
    unittest.main()
