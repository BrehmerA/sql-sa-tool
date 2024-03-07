import os
import sys
import unittest

from mock import patch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Appends the parent dir to the python path.

from main import Main


class MainTest(unittest.TestCase):


    # LANGUAGE
    def test_select_language_valid_input(self):
        test = Main()
        with patch('builtins.input', return_value='Python'):
            test.language = test._Main__validate_input(test.language, str(), lambda value: value == 'Java' or value == 'Python', str())
            self.assertEqual(test.language, 'Python')


    def test_select_language_invalid_input(self):
        test = Main()
        with patch('builtins.input', return_value=str()):
            test.language = test._Main__validate_input(test.language, str(), lambda value: value == 'Java' or value == 'Python', str())
            self.assertEqual(test.language, 'Java')


    # MIN NUMBER OF FOLLOWERS
    def test_select_min_number_of_followers_valid_input(self):
        test = Main()
        with patch('builtins.input', return_value='1'):
            test.min_number_of_followers = test._Main__validate_input(test.min_number_of_followers, str(), lambda value: int(value) >= 0, str())
            self.assertEqual(test.min_number_of_followers, '1')


    def test_select_min_number_of_followers_invalid_input(self):
        test = Main()
        with patch('builtins.input', side_effect=('-1', str())):
            test.min_number_of_followers = test._Main__validate_input(test.min_number_of_followers, str(), lambda value: int(value) >= 0, str())
            self.assertEqual(test.min_number_of_followers, 2)


    # MAX NUMBER OF FOLLOWERS
    def test_select_max_number_of_followers_valid_input(self):
        test = Main()
        with patch('builtins.input', return_value='3'):
            test.max_number_of_followers = test._Main__validate_input(test.max_number_of_followers, str(), lambda value: int(value) > int(test.min_number_of_followers), str())
            self.assertEqual(test.max_number_of_followers, '3')


    def test_select_max_number_of_followers_invalid_input(self):
        test = Main()
        with patch('builtins.input', side_effect=('-1', str())):
            test.max_number_of_followers = test._Main__validate_input(test.max_number_of_followers, str(), lambda value: int(value) > int(test.min_number_of_followers), str())
            self.assertIsNone(test.max_number_of_followers)


    # MIN SIZE
    def test_select_min_size_valid_input(self):
        test = Main()
        with patch('builtins.input', return_value='1'):
            test.min_size = test._Main__validate_input(test.min_size, str(), lambda value: int(value) >= 0, str())
            self.assertEqual(test.min_size, '1')


    def test_select_min_size_invalid_input(self):
        test = Main()
        with patch('builtins.input', side_effect=('-1', str())):
            test.min_size = test._Main__validate_input(test.min_size, str(), lambda value: int(value) >= 0, str())
            self.assertEqual(test.min_size, 100)


    # MAX SIZE
    def test_select_max_size_valid_input(self):
        test = Main()
        with patch('builtins.input', return_value='101'):
            test.max_size = test._Main__validate_input(test.max_size, str(), lambda value: int(value) > int(test.min_size), str())
            self.assertEqual(test.max_size, '101')


    def test_select_max_size_invalid_input(self):
        test = Main()
        with patch('builtins.input', side_effect=('-1', str())):
            test.max_size = test._Main__validate_input(test.max_size, str(), lambda value: int(value) > int(test.min_size), str())
            self.assertIsNone(test.max_size)


    # MIN NUMBER OF STARS
    def test_select_min_number_of_stars_valid_input(self):
        test = Main()
        with patch('builtins.input', return_value='1'):
            test.min_number_of_stars = test._Main__validate_input(test.min_number_of_stars, str(), lambda value: int(value) >= 0, str())
            self.assertEqual(test.min_number_of_stars, '1')


    def test_select_min_number_of_stars_invalid_input(self):
        test = Main()
        with patch('builtins.input', side_effect=('-1', str())):
            test.min_number_of_stars = test._Main__validate_input(test.min_number_of_stars, str(), lambda value: int(value) >= 0, str())
            self.assertEqual(test.min_number_of_stars, 2)


    # MAX NUMBER OF STARS
    def test_select_max_number_of_stars_valid_input(self):
        test = Main()
        with patch('builtins.input', return_value='3'):
            test.max_number_of_stars = test._Main__validate_input(test.max_number_of_stars, str(), lambda value: int(value) > int(test.min_number_of_stars), str())
            self.assertEqual(test.max_number_of_stars, '3')


    def test_select_max_number_of_stars_invalid_input(self):
        test = Main()
        with patch('builtins.input', side_effect=('-1', str())):
            test.max_number_of_stars = test._Main__validate_input(test.max_number_of_stars, str(), lambda value: int(value) > int(test.min_number_of_stars), str())
            self.assertIsNone(test.max_number_of_stars)


    # MIN NUMBER OF CONTRIBUTORS
    def test_select_min_number_of_contributors_valid_input(self):
        test = Main()
        with patch('builtins.input', return_value='1'):
            test.min_number_of_contributors = test._Main__validate_input(test.min_number_of_contributors, str(), lambda value: int(value) >= 0, str())
            self.assertEqual(test.min_number_of_contributors, '1')


    def test_select_min_number_of_contributors_invalid_input(self):
        test = Main()
        with patch('builtins.input', side_effect=('-1', str())):
            test.min_number_of_contributors = test._Main__validate_input(test.min_number_of_contributors, str(), lambda value: int(value) >= 0, str())
            self.assertEqual(test.min_number_of_contributors, 2)


    # MAX NUMBER OF CONTRIBUTORS
    def test_select_max_number_of_contributors_valid_input(self):
        test = Main()
        with patch('builtins.input', return_value='3'):
            test.max_number_of_contributors = test._Main__validate_input(test.max_number_of_contributors, str(), lambda value: int(value) > int(test.min_number_of_contributors), str())
            self.assertEqual(test.max_number_of_contributors, '3')


    def test_select_max_number_of_contributors_invalid_input(self):
        test = Main()
        with patch('builtins.input', side_effect=('-1', str())):
            test.max_number_of_contributors = test._Main__validate_input(test.max_number_of_contributors, str(), lambda value: int(value) > int(test.min_number_of_contributors), str())
            self.assertIsNone(test.max_number_of_contributors)


    # DEFINE SEARCH
    def test_define_search_valid_input(self):
        test = Main()
        with patch('builtins.input', side_effect=('Python', '1', '3', '1', '3', '1', '3', '1', '3')):
            test._Main__define_search()
            self.assertEqual(test.language, 'Python')
            self.assertEqual(test.min_number_of_followers, '1')
            self.assertEqual(test.max_number_of_followers, '3')
            self.assertEqual(test.min_size, '1')
            self.assertEqual(test.max_size, '3')
            self.assertEqual(test.min_number_of_stars, '1')
            self.assertEqual(test.max_number_of_stars, '3')
            self.assertEqual(test.min_number_of_contributors, '1')
            self.assertEqual(test.max_number_of_contributors, '3')


    def test_define_search_invalid_input(self):
        test = Main()
        with patch('builtins.input', side_effect=(str(), '-1', str(), '1', str(), '-1', str(), '1', str(), '-1', str(), '1', str(), '-1', str(), '1', str())):
            test._Main__define_search()
            self.assertEqual(test.language, 'Java')
            self.assertEqual(test.min_number_of_followers, 2)
            self.assertIsNone(test.max_number_of_followers)
            self.assertEqual(test.min_size, 100)
            self.assertIsNone(test.max_size)
            self.assertEqual(test.min_number_of_stars, 2)
            self.assertIsNone(test.max_number_of_stars)
            self.assertEqual(test.min_number_of_contributors, 2)
            self.assertIsNone(test.max_number_of_contributors)


    # SEARCH IDS
    def test_select_search_valid_input(self):
        test = Main()
        with patch('builtins.input', return_value='1'):
            test._Main__select_search()
            self.assertEqual(test.search_ids, ['1'])


    def test_select_search_invalid_input(self):
        test = Main()
        with patch('builtins.input', side_effect=('-1', '1')):
            test._Main__select_search()
            self.assertEqual(test.search_ids, ['1'])


if __name__ == '__main__':
    unittest.main()
