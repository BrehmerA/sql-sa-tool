import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) # Appends the parent dir to the python path.

from search import Search


def get_search_object():
    return Search('Java', 2, None, 100, None, 2, None, 2, None)


def get_output(test):
    return test._Search__request('https://api.github.com/search/repositories?q=language:Java')


class SearchTest(unittest.TestCase):


    def test_request(self):
        test = get_search_object()
        self.assertIsNotNone(get_output(test))


    def test_remove_tabs_and_new_lines(self):
        test = get_search_object()
        self.assertEqual(test._Search__remove_tabs_and_new_lines('\t\n'), '')


    def test_extract_content(self):
        test = get_search_object()
        self.assertIsNotNone(test._Search__extract_content(get_output(test)))


    def test_extract_next_url(self):
        test = get_search_object()
        self.assertIsNotNone(test._Search__extract_next_url(get_output(test)))


if __name__ == '__main__':
    unittest.main()
