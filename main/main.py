from search import Search


class Main:
    """The program's main class - responsible for execution."""

    language = 'Python'
    min_number_of_followers = 2
    max_number_of_followers = None
    min_size = 100 # kB
    max_size = None
    min_number_of_stars = 2
    max_number_of_stars = None
    min_number_of_contributors = 2
    max_number_of_contributors = None


    def __define_search(self):
        print('You will now be presented a number of options to define your search. The value inside the parentheses is the default. Press Enter to select the default value, otherwise input your preferred value and press Enter.')

        value = input(f'Language: ({self.language}) ')
        if len(value) > 0: # TODO Add validation.
            self.language = value
        value = input(f'Minimum number of followers: ({self.min_number_of_followers}) ')
        if len(value) > 0:
            self.min_number_of_followers = value
        value = input(f'Maximum number of followers: ')
        if len(value) > 0:
            self.max_number_of_followers = value
        value = input(f'Minimum size: ({self.min_size}) ')
        if len(value) > 0:
            self.min_size = value
        value = input(f'Maximum size: ')
        if len(value) > 0:
            self.max_size = value
        value = input(f'Minimum number of stars: ({self.min_number_of_stars}) ')
        if len(value) > 0:
            self.min_number_of_stars = value
        value = input(f'Maximum number of stars: ')
        if len(value) > 0:
            self.max_number_of_stars = value
        value = input(f'Minimum number of contributors: ({self.min_number_of_contributors}) ')
        if len(value) > 0:
            self.min_number_of_contributors = value
        value = input(f'Maximum number of contributors: ')
        if len(value) > 0:
            self.max_number_of_contributors = value

        print("You've selected the following values:", self.language, self.min_number_of_followers, self.max_number_of_followers, self.min_size, self.max_size, self.min_number_of_stars, self.max_number_of_stars, self.min_number_of_contributors, self.max_number_of_contributors)


    def run(self):
        """Main method for executing the program."""

        self.__define_search()
        search = Search(self.language, self.min_number_of_followers, self.max_number_of_followers, self.min_size, self.max_size, self.min_number_of_stars, self.max_number_of_stars, self.min_number_of_contributors, self.max_number_of_contributors)
        search.search_repositories()
        search.filter_on_min_number_of_contributors()


if __name__ == '__main__':
    Main().run()
