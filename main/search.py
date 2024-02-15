import shlex
import subprocess
from pathlib import Path
from time import sleep


class Search:
    """Responsible for searching for reposititories.

    The selection will be based on provided query arguments.
    """

    PATH_TO_TOKEN = Path(__file__).resolve().parent / '.token'
    LANGUAGES = ('Java', 'Python')
    MIN_NUMBER_OF_FOLLOWERS = 2
    MIN_SIZE = 100 # kB
    MIN_NUMBER_OF_STARS = 2
    NUMBER_OF_RESULTS_PER_PAGE = 4 # Max is 100.
    token = None
    api = None


    def __init__(self):
        """The constructor..."""

        with open(self.PATH_TO_TOKEN) as file:
            self.token = file.read()


    def get_all_repositories(self):
        # The requests library doesn't support pagination.
        # The API wrapper GhApi wasn't working either since it couldn't find all the repositories.
        # We therefore went with the subprocess approach, to be able to run curl commands in the terminal.

        args = shlex.split(f'''curl --include --request GET --url "https://api.github.com/search/repositories?q=language:{self.LANGUAGES[1]}+followers:>{self.MIN_NUMBER_OF_FOLLOWERS}+size:>{self.MIN_SIZE}+stars:>{self.MIN_NUMBER_OF_STARS}&s=stars&o=desc&per_page={self.NUMBER_OF_RESULTS_PER_PAGE}" --header "Accept: application/vnd.github+json" --header "Authorization: Bearer {self.token}"''')
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        stdout, stderr = process.communicate()
        output = stdout.decode('utf-8')

        # Extracts the link header.
        links = output.split('link: ')[1]
        links = links.split('x-github-api-version-selected: ')[0] # The header following the link header.
        links = links.split(', ') # Separates the links.
        urls = {} # For storing the values with their urls.
        for link in links:
            link = link.split('>; rel="') # Separates the url and the value.
            url = link[0][1:] # Removes the initial <.
            value = link[1].replace('"', '') # Removes the ending ".
            value = ''.join(c for c in value if ord(c)>31 and ord(c)<126) # Removes tabs and new lines.
            urls[value] = url # Saves the value with its url.
        for key, value in urls.items():
            print(key, value)

        # Extracts the content.
        output = output.splitlines()
        start = None
        for index in range(0, len(output)):
            line = output[index]
            if line == '{':
                start = index
                break
        if start is not None:
            output = output[index:]
            for line in output: print(line)
            # TODO Turn into JSON.
        else:
            print("The content couldn't be extracted.")
            exit()

        # TODO For each language: For each repo in each page: Save to the DB.
        # TODO Then filter further on minimum number of contributors. Delete repos that don't meet the critera from the DB.


if __name__ == '__main__':
    Search().get_all_repositories()
