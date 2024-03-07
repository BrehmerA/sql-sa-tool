import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Appends the parent dir to the python path.

from analysis import Analysis


class AnalysisTest(unittest.TestCase):
    
    def test_init(self):
        analyse = Analysis()
        self.assertIsNotNone(analyse.DB._Database__CONNECTION)
        self.assertIsNotNone(analyse.DB._Database__CURSOR)
        self.assertTrue(os.path.exists(os.getcwd() + '/cloned'))

    def test_getRepos(self):
        analyse = Analysis()
        repos = analyse.__getRepos('Python', 999)
        self.assertEqual(repos, [])

if __name__ == '__main__':
    unittest.main()
