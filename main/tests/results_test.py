import os
import sys
import io
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Appends the parent dir to the python path.

from results import Results


class ResultsTest(unittest.TestCase):
    """Unit tests for result class"""

    """def test_print_to_screen(self):
        sys.stdout = sys.__stdout__
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        res = Results((99999,))
        res.print_to_screen()
        sys.stdout = sys.__stdout__
        self.assertTrue(len(capturedOutput.getvalue()!=0))"""


    def test_write_to_file(self):
        res = Results((99999,))
        res.write_to_file()



if __name__ == '__main__':
    pass
