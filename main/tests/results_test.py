import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Appends the parent dir to the python path.

from main.results import Results


class ResultsTest(unittest.TestCase):
    pass


if __name__ == '__main__':
    pass