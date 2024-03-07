import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Appends the parent dir to the python path.

from database.database import Database


class DatabaseTest(unittest.TestCase):


    def test_connect(self):
        db = Database()
        db.connect()
        self.assertIsNotNone(db._Database__CONNECTION)
        self.assertIsNotNone(db._Database__CURSOR)
        db.close()


    def test_close(self):
        db = Database()
        db.connect()
        db.close()
        self.assertIsNone(db._Database__CONNECTION)
        self.assertIsNone(db._Database__CURSOR)


    def test_fetch_one(self):
        db = Database()
        db.connect()
        name = db.fetch_one('''SELECT name FROM language WHERE id = 1''')
        self.assertEqual(name, ('Java', ))
        db.close()


    def test_fetch_all(self):
        db = Database()
        db.connect()
        names = db.fetch_all('''SELECT name FROM language ORDER BY id ASC''')
        self.assertEqual(names, [('Java', ), ('Python', )])
        db.close()


    def test_execute(self):
        db = Database()
        db.connect()
        db.execute('''CREATE TABLE test(id INTEGER PRIMARY KEY, value TEXT NOT NULL)''')
        table = db.fetch_one('''SELECT name FROM sqlite_master WHERE type = 'table' AND name = ?''', ('test', ))
        self.assertEqual(table, ('test', ))
        db.close()


    def test_last_row_id(self):
        db = Database()
        db.connect()
        db.execute('''INSERT INTO test(value) VALUES (?)''', ('test', ))
        id = db.last_row_id()
        self.assertEqual(id, 1)
        db.execute('''DROP TABLE test''')
        db.close()


if __name__ == '__main__':
    unittest.main()
