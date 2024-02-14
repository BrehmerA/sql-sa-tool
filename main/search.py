from pathlib import Path

from ghapi.all import GhApi


class Search:
    """Responsible for searching for reposititories.

    The selection will be based on provided query arguments.
    """

    PATH_TO_TOKEN = Path(__file__).resolve().parent / '.token'
    MIN_NUMBER_OF_FOLLOWERS = 2
    LANGUAGES = ('Java', 'Python')
    MIN_SIZE = 100 # kB
    MIN_NUMBER_OF_STARS = 2 # 1000
    token = None
    api = None


    def __init__(self):
        """The constructor..."""

        with open(self.PATH_TO_TOKEN) as file:
            token = file.read()

        self.api = GhApi(token=token)


    def get_all_repositories(self):
        # 60 requests per hour if unauthenticated. Otherwise 5000 requests/hour.

        # We'll have to use a wrapper, called GhApi, for GitHub's REST API, since pagination isn't supported with the requests library.

        repos = self.api.search.repos(q=f'q=followers:>{self.MIN_NUMBER_OF_FOLLOWERS} language:{self.LANGUAGES[1]} size:>{self.MIN_SIZE} stars:>{self.MIN_NUMBER_OF_STARS}', per_page=1, page=1)
        print(repos)

        # TODO For each language: For each repo in each page: Save to the DB.
        # TODO Then filter further on minimum number of contributors. Delete repos that don't meet the critera from the DB.


if __name__ == '__main__':
    Search().get_all_repositories()
