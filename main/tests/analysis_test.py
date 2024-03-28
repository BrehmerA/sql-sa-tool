import os
import sys
import unittest
from time import sleep

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Appends the parent dir to the python path.

from analysis import Analysis
from database.database import Database


class AnalysisTest(unittest.TestCase):
    """Test class for analyzing repositories."""

    __analysis = Analysis()


    @classmethod
    def setUpClass(cls):
        DB = Database()
        DB.connect()
        try:
            DB.execute(f'''
            INSERT OR IGNORE INTO repository (id, name, url, size, number_of_stars, number_of_contributors) VALUES (?, ?, ?, ?, ?, ?)
            ''', (759767437, 'sql-repo-tester', 'https://api.github.com/repos/BrehmerA/sql-repo-tester', 394, 0, 1))
        except:
            pass

        try:
            DB.execute(f'''INSERT OR IGNORE INTO search
                (id, date, language, min_number_of_stars, max_number_of_stars, min_number_of_contributors, min_size)
                VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (10001, '2024-03-01', 1, 20, 100, 2, 100))
        except:
            pass

        try:
            DB.execute(f'''INSERT OR IGNORE INTO search
                (id, date, language, min_number_of_stars, max_number_of_stars, min_number_of_contributors, min_size)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (10002, '2024-03-01', 2, 20, 100, 2, 100))
        except:
            pass

        try:
            DB.execute('''DELETE from result WHERE search=10001''')
            DB.execute('''DELETE from search_repository WHERE search=10001''')
            DB.execute('''INSERT OR IGNORE INTO search_repository (search, repository) VALUES (?, ?)''', (10001, 759767437))
        except:
            pass
        try:
            DB.execute('''DELETE from result WHERE search=10002''')
            DB.execute('''DELETE from search_repository WHERE search=10002''')
            DB.execute('''INSERT OR IGNORE INTO search_repository (search, repository) VALUES (?, ?)''', (10002, 759767437))
        except:
            pass

        DB.close()


    def test_init(self):
        """Test init. DB initialise and folder created correctly."""

        self.assertTrue(os.path.exists(os.getcwd() + '/cloned'))


    def test_filter_and_analyse(self):
        """Test run through with analyzing and writing result to DB."""

        self.__analysis.start_filter(10001)
        DB=Database()
        DB.connect()
        res = DB.fetch_all('''SELECT * from result WHERE search=10001''')
        DB.close()
        self.assertTrue(len(res)==1)


if __name__ == '__main__':
    unittest.main()
