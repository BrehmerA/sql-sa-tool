import json
import shlex
import subprocess
from datetime import date, datetime
from pathlib import Path
from sys import platform
from time import sleep

from database.database import Database
from multiprocess import Process


class Search:
    """Responsible for searching for reposititories.

    The selection will be based on provided query arguments.
    """

    DB = Database()
    PATH_TO_TOKEN = Path(__file__).resolve().parent / '.token'
    NUMBER_OF_RESULTS_PER_PAGE = 100 # Max is 100.

    token = None

    language = None
    min_size = None
    max_size = None
    min_number_of_stars = None
    max_number_of_stars = None
    number_of_stars = None
    min_number_of_contributors = None
    max_number_of_contributors = None


    def __init__(self, language, min_size, max_size, min_number_of_stars, max_number_of_stars, number_of_stars, min_number_of_contributors, max_number_of_contributors):
        """The constructor..."""

        self.language = language
        self.min_size = min_size
        self.max_size = max_size
        self.min_number_of_stars = min_number_of_stars
        self.max_number_of_stars = max_number_of_stars
        self.number_of_stars = number_of_stars
        self.min_number_of_contributors = min_number_of_contributors
        self.max_number_of_contributors = max_number_of_contributors

        with open(self.PATH_TO_TOKEN) as file:
            self.token = file.read()


    def __request(self, url):
        args = shlex.split(f'''curl --include --request GET --url "{url}" --header "Accept: application/vnd.github+json" --header "Authorization: Bearer {self.token}"''')
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        stdout, stderr = process.communicate()
        return stdout.decode('utf-8')


    def __remove_tabs_and_new_lines(self, string):
        """Removes tabs and new lines from a string."""

        return ''.join(character for character in string if ord(character) >= 32 and ord(character) <= 122)


    def __extract_content(self, output):
        lines = output.splitlines()
        start = None
        for index in range(0, len(lines)):
            line = lines[index]
            if line == '{' or line == '[':
                start = index
                break
        if start is None:
            rate_limit = output.split('x-ratelimit-remaining: ')[1]
            rate_limit = self.__remove_tabs_and_new_lines(rate_limit)
            rate_limit = rate_limit.split('x-ratelimit-reset: ')
            if int(rate_limit[0]) == 0:
                rate_limit = rate_limit[1].split('x-ratelimit-used: ')[0]
                print(f"You've exceeded the rate limit. Wait until {datetime.fromtimestamp(int(rate_limit))} til you try again.")
            else: print("The content couldn't be extracted.")
            exit()
        return json.loads(''.join(lines[start:]))


    def __extract_repositories(self, content, search_id):
        number_of_extracted_repositories = 0
        for repository in content['items']:
            repository_id = repository['id']
            repository_name = repository['name']
            repository_url = repository['url']
            repository_size = repository['size']
            repository_number_of_stars = repository['stargazers_count']
            # Saves the repository:
            self.DB.connect()
            exists = self.DB.fetch_one('''SELECT id FROM repository WHERE id = ?''', (repository_id, ))
            exists = False if exists is None else exists[0] == repository_id
            if not exists:
                self.DB.execute('''INSERT INTO repository(id, name, url, size, number_of_stars) VALUES (?, ?, ?, ?, ?)''', (repository_id, repository_name, repository_url, repository_size, repository_number_of_stars))
                self.DB.execute('''INSERT INTO search_repository(search, repository) VALUES (?, ?)''', (search_id, repository_id))
                number_of_extracted_repositories += 1
                print(repository_id, repository_name, repository_url, repository_size, repository_number_of_stars)
            self.DB.close()
        return number_of_extracted_repositories


    def __extract_next_url(self, output):
        link_header = 'link: ' if platform == 'darwin' else 'Link: '
        links = output.split(link_header)
        if len(links) > 1:
            links = output.split(link_header)[1]
            links = links.split('x-github-api-version-selected: ')[0] # The header following the link header.
            links = links.split(', ') # Separates the links.
            for link in links:
                link = link.split('>; rel="') # Separates the url and the value.
                url = link[0][1:] # Removes the initial <.
                value = link[1].replace('"', '') # Removes the ending ".
                value = self.__remove_tabs_and_new_lines(value)
                if value == 'next': return url
        return None


    def __search_repositories(self):
        # The requests library doesn't support pagination.
        # The API wrapper GhApi wasn't working either since it couldn't find all the repositories.
        # We therefore went with the subprocess approach, to be able to run curl commands in the terminal.

        # Even with pagination the number of results is limited to 1000.
        # We can probably go around this by using different values for order_by and sort.
        # We can also define an exact number of stars, as well as size, instead of above/below a certain value.

        # curl --include --request GET --url "https://api.github.com/search/repositories?q=language:Python+size:>99+stars:2+-is:fork&per_page=100" --header "Accept: application/vnd.github+json"

        size = f"size:{f'>{self.min_size - 1}' if self.max_size is None else f'{self.min_size}..{self.max_size}'}"
        stars = f"stars:{f'{self.number_of_stars}' if self.number_of_stars is not None else f'{self.min_number_of_stars}..{self.max_number_of_stars}' if self.max_number_of_stars is not None else f'>{self.min_number_of_stars - 1}'}"
        url = f"https://api.github.com/search/repositories?q=language:{self.language}+{size}+{stars}+-is:fork&per_page={self.NUMBER_OF_RESULTS_PER_PAGE}"

        # Saves the search.
        self.DB.connect()
        self.DB.execute('''INSERT INTO search(date, language, min_size, max_size, min_number_of_stars, max_number_of_stars, number_of_stars, min_number_of_contributors, max_number_of_contributors) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (date.today(), 1 if self.language == 'Java' else 2, self.min_size, self.max_size, self.min_number_of_stars, self.max_number_of_stars, self.number_of_stars, self.min_number_of_contributors, self.max_number_of_contributors))
        search_id = self.DB.last_row_id()
        self.DB.close()

        total_number_of_extracted_repositories = 0

        while (url is not None):
            output = self.__request(url)
            content = self.__extract_content(output)
            number_of_extracted_repositories = self.__extract_repositories(content, search_id)
            total_number_of_extracted_repositories += number_of_extracted_repositories
            url = self.__extract_next_url(output)
            sleep(2) # In order to adhere to the rate limit of 30 authenticated requests per minute.

        print(total_number_of_extracted_repositories)

        return search_id


    def __filter_on_min_number_of_contributors(self, search_id):

        def filter_on_min_number_of_contributors(repositories, i):
            DB = Database()
            DB.connect()
            for j in range(len(repositories)):
                repository = repositories[j]
                id = repository[0]
                name = repository[1]
                url = f'{repository[2]}/contributors?per_page={int(self.min_number_of_contributors)+1}'
                output = self.__request(url)
                content = self.__extract_content(output)
                try:
                    message = content['message']
                    print(message)
                    for i in range(0,240):
                        print('Waiting for rate limit cool down: ',204-i,'s')
                        sleep(1)
                except:
                    number_of_contributors = len(content) # TODO Not the actual number.
                    if number_of_contributors >= int(self.min_number_of_contributors) and (self.max_number_of_contributors is None or number_of_contributors <= int(self.max_number_of_contributors)):
                        DB.execute('''UPDATE repository SET number_of_contributors = ? WHERE id = ?''', (number_of_contributors, id))
                        print(f'{i}: Updated the repository with id {id} and name {name} in the DB.')
                    else:
                        DB.execute('''DELETE FROM search_repository WHERE repository = ?''', (id, ))
                        DB.execute('''DELETE FROM repository WHERE id = ?''', (id, ))
                        print(f'{i}: Deleted the repository with id {id} and name {name} from the DB.')
                finally:
                    i += 1
            DB.close()

        self.DB.connect()
        repositories = self.DB.fetch_all('''SELECT DISTINCT r.* FROM repository AS r LEFT JOIN search_repository sr ON r.id=sr.repository WHERE sr.search = ?''', (search_id, ))
        self.DB.close()
        splits = []
        for i in range(0, 1000, 250):
            try:
                split = repositories[i:i + 250]
                splits.append(split)
            except:
                split = repositories[i:len(repositories)]
                splits.append(split)
                break
        processes = []
        for i in range(len(splits)):
            split = splits[i]
            process = Process(target=filter_on_min_number_of_contributors, args=(split, i * 250))
            processes.append(process)
            process.start()
        for process in processes:
            process.join()


    def run(self):
        search_id = self.__search_repositories()
        self.__filter_on_min_number_of_contributors(search_id) # TODO How can filtering on min number of contributors be made more effective?
        return search_id
