import os
import sys
import unittest
import uuid

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Appends the parent dir to the python path.
from database.database import Database
from analysis import Analysis



class AnalysisTest(unittest.TestCase):

    __analysis = Analysis()

    @classmethod
    def setUpClass(cls):
        DB = Database()
        DB.connect()
        try:
            DB.execute(f'''
            INSERT INTO repository (id, name, url, number_of_followers, size, number_of_stars, number_of_contributors) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (759767437, 'sql-repo-tester', 'https://api.github.com/repos/BrehmerA/sql-repo-tester', 1, 394, 0, 1))
        except:
            pass
        
        try:
            DB.execute(f'''INSERT INTO search 
                (id, date, language, min_number_of_followers, max_number_of_followers, min_number_of_stars, max_number_of_stars, min_number_of_contributors, min_size)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (10001, '2024-03-01', 1, 2, 10, 20, 100, 2, 100))
        except:
            pass
        
        try:
            DB.execute(f'''INSERT INTO search 
                (id, date, language, min_number_of_followers, max_number_of_followers, min_number_of_stars, max_number_of_stars, min_number_of_contributors, min_size)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (10002, '2024-03-01', 2, 2, 10, 20, 100, 2, 100))
        except:
            pass

        try:
            DB.execute('''INSERT INTO search_repository (search, repository) VALUES (?, ?)''', (10001, 759767437))
        except:
            pass
        try:
            DB.execute('''INSERT INTO search_repository (search, repository) VALUES (?, ?)''', (10002, 759767437))
        except:
            pass

        DB.close()

    def test_init(self):
        self.assertIsNotNone(self.__analysis.DB._Database__CONNECTION)
        self.assertIsNotNone(self.__analysis.DB._Database__CURSOR)
        self.assertTrue(os.path.exists(os.getcwd() + '/cloned'))

    def test_getRepos(self):
        self.assertEqual(self.__analysis.getRepos('Python', 10002), [['https://github.com/BrehmerA/sql-repo-tester.git', 759767437]])
        self.assertEqual(self.__analysis.getRepos('Java', 10001), [['https://github.com/BrehmerA/sql-repo-tester.git', 759767437]])

if __name__ == '__main__':
    unittest.main()
