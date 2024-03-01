import os
import sys
import unittest
from io import StringIO
from mock import patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Appends the parent dir to the python path.

from main import Main


class MainTest(unittest.TestCase):


    def test_validate_input(self):
        test = Main()
        with patch('builtins.input', return_value='Python'), patch('sys.stdout', new=StringIO()):
            test.language = test._Main__validate_input('Java', f'Language: ({test.language}) ', lambda value: value == 'Java' or value == 'Python', 'Not a valid input.')
            self.assertEqual(test.language, 'Python')


if __name__ == '__main__':
    unittest.main()
