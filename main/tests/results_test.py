import csv
import os
import sys
import io
import unittest
import glob

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Appends the parent dir to the python path.

from results import Results

expectedFileOutput = '''Search id included in results,99999
Number of repos searched,11
Number of repos analyzed,8
Number of repos with found SQLIV,3
Number of repos without found SQLIV,5
Start of found SQLIV by language in analyzed repos
Python,3
Start of no SQLIV by language in analyzed repos
Python,5
Start of repos with found SQLIV
Repo id,stars,followers,size,contributors,number of found SQLIV
26554,16742,16742,40093,3,2
46939,7853,7853,7696,3,1
54383,185,185,701,3,1
Start of raw results
Search id,Repo id,SQLIV,stars,followers,size,contributors,file,location
99999,26554,1,16742,16742,40093,3,main/c1.py,"10,1,10,5"
99999,26554,1,16742,16742,40093,3,main/c2.py,"10,1,10,5"
99999,46939,1,7853,7853,7696,3,main/c3.py,"10,1,10,5"
99999,54383,1,185,185,701,3,main/c4.py,"10,1,10,5"
99999,57419,0,5866,5866,1752,3,,
99999,71978,0,139,139,224,3,,
99999,79012,0,139,139,340,3,,
99999,100428,0,251,251,362,3,,
99999,107258,0,15850,15850,801,3,,
'''

class ResultsTest(unittest.TestCase):
    """Unit tests for result class"""

    def test_print_to_screen(self):
        """Test print to screen"""
        sys.stdout = sys.__stdout__
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        res = Results((99999,))
        res.print_to_screen()
        sys.stdout = sys.__stdout__
        expectedOut=('''------Results From Analysis-----
Searches included in result compilation: (99999,)
Total number of repos in search:         11
Total number of analyzed repos:          8
Total number of repos with SQLiv:s       3 ( 37.5 %)
Analyzed repos without SQLiv:s found     5
Python repos with SQLiv                        3
Python repos without SQLiv                     5
''')
        self.assertEqual(capturedOutput.getvalue(), expectedOut)


    def test_write_to_file(self):
        """Test csv file creation"""
        self.maxDiff=None
        res = Results((99999,))
        result = len(glob.glob(f'*.csv'))
        res.write_to_file()
        result_files = glob.glob(f'resultCSV*.csv')
        after = len(result_files)
        self.assertTrue(after-result == 1)
        latest=max(result_files, key=os.path.getctime)
        with open(latest) as results:
            fileRes = results.read()
        self.assertEqual(fileRes, expectedFileOutput)




if __name__ == '__main__':
    unittest.main()
