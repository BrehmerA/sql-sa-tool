import json
import shlex
import subprocess
from datetime import date
from pathlib import Path
from time import sleep

from database.database import Database


class Search:
    """Responsible for searching for reposititories.

    The selection will be based on provided query arguments.
    """

    DB = Database()
    PATH_TO_TOKEN = Path(__file__).resolve().parent / '.token'
    NUMBER_OF_RESULTS_PER_PAGE = 100 # Max is 100.

    token = None

    language = None
    min_number_of_followers = None
    max_number_of_followers = None
    min_size = None
    max_size = None
    min_number_of_stars = None
    max_number_of_stars = None
    min_number_of_contributors = None
    max_number_of_contributors = None


    def __init__(self, language, min_number_of_followers, max_number_of_followers, min_size, max_size, min_number_of_stars, max_number_of_stars, min_number_of_contributors, max_number_of_contributors):
        """The constructor..."""

        self.language = language
        self.min_number_of_followers = min_number_of_followers
        self.max_number_of_followers = max_number_of_followers
        self.min_size = min_size
        self.max_size = max_size
        self.min_number_of_stars = min_number_of_stars
        self.max_number_of_stars = max_number_of_stars
        self.min_number_of_contributors = min_number_of_contributors
        self.max_number_of_contributors = max_number_of_contributors

        self.DB.connect()

        with open(self.PATH_TO_TOKEN) as file:
            self.token = file.read()

        self.__search_repositories()
        self.__filter_on_min_number_of_contributors()

        self.DB.close()


    def __request(self, url):
        args = shlex.split(f'''curl --include --request GET --url "{url}" --header "Accept: application/vnd.github+json" --header "Authorization: Bearer {self.token}"''')
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        stdout, stderr = process.communicate()
        return stdout.decode('utf-8')


    def __extract_content(self, output):
        output = output.splitlines()
        start = None
        for index in range(0, len(output)):
            line = output[index]
            if line == '{' or line == '[':
                start = index
                break
        if start is None:
            print("The content couldn't be extracted.")
            exit()
        return json.loads(''.join(output[start:]))


    def __extract_repositories(self, content, search_id):
        for repository in content['items']:
            repository_id = repository['id']
            repository_name = repository['name']
            repository_url = repository['url']
            # repository_html_url = repository['html_url']
            repository_number_of_followers = repository['watchers_count']
            repository_size = repository['size']
            repository_number_of_stars = repository['stargazers_count']
            print(repository_id, repository_name, repository_url, repository_number_of_followers, repository_size, repository_number_of_stars)
            # Saves the repository:
            exists = self.DB.fetch_one('''SELECT id FROM repository WHERE id = ?''', (repository_id, )) != None
            if not exists:
                self.DB.execute('''INSERT INTO repository(id, name, url, number_of_followers, size, number_of_stars) VALUES (?, ?, ?, ?, ?, ?)''', (repository_id, repository_name, repository_url, repository_number_of_followers, repository_size, repository_number_of_stars))
            self.DB.execute('''INSERT INTO search_repository(search, repository) VALUES (?, ?)''', (search_id, repository_id))


    def __extract_next_url(self, output):
        links = output.split('link: ')[1]
        links = links.split('x-github-api-version-selected: ')[0] # The header following the link header.
        links = links.split(', ') # Separates the links.
        for link in links:
            link = link.split('>; rel="') # Separates the url and the value.
            url = link[0][1:] # Removes the initial <.
            value = link[1].replace('"', '') # Removes the ending ".
            value = ''.join(c for c in value if ord(c)>31 and ord(c)<126) # Removes tabs and new lines.
            if value == 'next': return url
        return None


    def __search_repositories(self):
        # The requests library doesn't support pagination.
        # The API wrapper GhApi wasn't working either since it couldn't find all the repositories.
        # We therefore went with the subprocess approach, to be able to run curl commands in the terminal.

        # Even with pagination the number of results is limited to 1000.
        # We can probably go around this by using different values for order_by and sort.
        # We can also define an exact number of followers/stars, as well as size, instead of above/below a certain value.

        # curl --include --request GET --url "https://api.github.com/search/repositories?q=language:Python+followers:>2+size:>100+stars:>2&s=stars&o=desc&per_page=100" --header "Accept: application/vnd.github+json"

        # for language in self.LANGUAGES:
        url = f"https://api.github.com/search/repositories?q=language:{self.language}+followers:>{self.min_number_of_followers}{f'+followers:<{self.max_number_of_followers}' if self.max_number_of_followers is not None else ''}+size:>{self.min_size}{f'+size:<{self.max_size}' if self.max_size is not None else ''}+stars:>{self.min_number_of_stars}{f'+stars:<{self.max_number_of_stars}' if self.max_number_of_stars is not None else ''}&s=stars&o=desc&per_page={self.NUMBER_OF_RESULTS_PER_PAGE}"

        # Saves the search.
        self.DB.execute('''INSERT INTO search(date, language, min_number_of_followers, max_number_of_followers, min_size, max_size, min_number_of_stars, max_number_of_stars, min_number_of_contributors, max_number_of_contributors) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (date.today(), 1 if self.language == 'Java' else 2, self.min_number_of_followers, self.max_number_of_followers, self.min_size, self.max_size, self.min_number_of_stars, self.max_number_of_stars, self.min_number_of_contributors, self.max_number_of_contributors))
        search_id = self.DB.fetch_one('''SELECT MAX(id) FROM search''')[0]

        while (url is not None):
            output = self.__request(url)
            content = self.__extract_content(output)
            self.__extract_repositories(content, search_id)
            url = self.__extract_next_url(output)
            sleep(2) # In order to adhere to the rate limit of 30 authenticated requests per minute.


    def __filter_on_min_number_of_contributors(self):
        repositories = self.DB.fetch_all('''SELECT * FROM repository''')
        for repository in repositories:
            id = repository[0]
            name = repository[1]
            url = f'{repository[2]}/contributors?per_page={self.min_number_of_contributors+1}'
            output = self.__request(url)
            content = self.__extract_content(output)
            message = None
            try:
                message = content['message']
            except:
                number_of_contributors = len(content)
                if number_of_contributors >= self.min_number_of_contributors and (self.max_number_of_contributors is None or number_of_contributors <= self.max_number_of_contributors):
                    self.DB.execute('''UPDATE repository SET number_of_contributors = ? WHERE id = ?''', (number_of_contributors, id))
                    print(f'Updated the repository with id {id} and name {name} in the DB.')
                else:
                    self.DB.execute('''DELETE FROM search_repository WHERE repository = ?''', (id, ))
                    self.DB.execute('''DELETE FROM repository WHERE id = ?''', (id, ))
                    print(f'Deleted the repository with id {id} and name {name} from the DB.')
            if message is not None: print(message)
            sleep(2) # In order to adhere to the rate limit. # TODO Look up if another rate limit applies to this endpoint.
