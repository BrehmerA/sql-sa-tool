from database.database import Database
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


    def __validate_input(self, message, boolean, error_message):
        while True:
            value = input(message)
            if len(value) > 0:
                if boolean(value):
                    return value
                print(f'{error_message} Please try again.')
                continue
            break


    def __define_search(self):
        print('You will now be presented a number of options to define your search. The value inside the parentheses is the default. Press Enter to select the default value, otherwise input your preferred value and press Enter.')

        self.language = self.__validate_input(f'Language: ({self.language}) ', lambda value: value == 'Java' or value == 'Python', 'Not a valid input.')
        self.min_number_of_followers = self.__validate_input(f'Minimum number of followers: ({self.min_number_of_followers}) ', lambda value: int(value) >= 0, 'The value has to be equal to or greater than 0.')
        self.max_number_of_followers = self.__validate_input(f'Maximum number of followers: ', lambda value: int(value) > int(self.min_number_of_followers), 'The value has to be greater than the min value.')
        self.min_size = self.__validate_input(f'Minimum size: ({self.min_size}) ', lambda value: int(value) >= 0, 'The value has to be equal to or greater than 0.')
        self.max_size = self.__validate_input(f'Maximum size: ', lambda value: int(value) > int(self.min_size), 'The value has to be greater than the min value.')
        self.min_number_of_stars = self.__validate_input(f'Minimum number of stars: ({self.min_number_of_stars}) ', lambda value: int(value) >= 0, 'The value has to be equal to or greater than 0.')
        self.max_number_of_stars = self.__validate_input(f'Maximum number of stars: ', lambda value: int(value) > int(self.min_number_of_stars), 'The value has to be greater than the min value.')
        self.min_number_of_contributors = self.__validate_input(f'Minimum number of contributors: ({self.min_number_of_contributors}) ', lambda value: int(value) >= 0, 'The value has to be equal to or greater than 0.')
        self.max_number_of_contributors = self.__validate_input(f'Maximum number of contributors: ', lambda value: int(value) > int(self.min_number_of_contributors), 'The value has to be greater than the min value.')

        print("You've selected the following values:", self.language, self.min_number_of_followers, self.max_number_of_followers, self.min_size, self.max_size, self.min_number_of_stars, self.max_number_of_stars, self.min_number_of_contributors, self.max_number_of_contributors)


    def __select_search(self):
        db = Database()
        db.connect()

        searches = db.fetch_all('''SELECT * FROM search''')
        print('ID\tDATE\t\tLANGUAGE\tMIN NUMBER OF FOLLOWERS\t\tMAX NUMBER OF FOLLOWERS\tMIN SIZE\tMAX SIZE\tMIN NUMBER OF STARS\tMAX NUMBER OF STARS\tMIN NUMBER OF CONTRIBUTORS\tMAX NUMBER OF FOLLOWERS')
        search_id_list = []
        for search in searches:
            search_id_list.append(search[0])
            string = str()
            for index in range(0, len(search)):
                value = search[index]
                sep = str()
                match index:
                    case 2:
                        sep = '\t\t'
                    case 3:
                        sep = '\t\t\t\t'
                    case 4:
                        sep = '\t\t\t\t\t'
                    case _:
                        sep = '\t'
                string += f'{value}{sep}'
            print(string)
        search_id = None
        while search_id is None:
            value = input('Please enter the ID of the search you want to be presented: ')
            if len(value) > 0 and int(value) in search_id_list:
                search_id = value
            else:
                print('Not a valid input. Please try again.')
        print(f"You've selected the following ID: {search_id}.")

        db.close()


    def run(self):
        """Main method for executing the program."""

        self.__define_search()
        # Search(self.language, self.min_number_of_followers, self.max_number_of_followers, self.min_size, self.max_size, self.min_number_of_stars, self.max_number_of_stars, self.min_number_of_contributors, self.max_number_of_contributors)

        self.__select_search()


if __name__ == '__main__':
    Main().run()
