from analysis import Analysis
from database.database import Database
from results import Results
from search import Search


class Main:
    """The program's main class - responsible for execution."""

    language = 'Java'
    computer = 1
    min_size = 100 # kB (i.e., 0.1 MB)
    max_size = None # 1000000 # kB (i.e., 1 GB)
    min_number_of_stars = 2
    max_number_of_stars = None
    min_number_of_contributors = 2
    max_number_of_contributors = None

    search_ids = []

    Search_java = {
        'stars' : (6,11,36),
        'size' : ((300,410,2000,10000,15000,100000,300000,700000,-1),(500,1000,5000,10000,50000,100000,-1),(500,5000,50000,100000,-1)),
        'steps' : ((0,5,10,50,250,500,10000,50000,-1),(10,50,100,1000,5000,10000,-1),(50,500,5000,50000,-1)),
    }

    Search_python = {
        'stars' : (6,11,21,66),
        'size' : ((300,400,2000,10000,15000,100000,300000,700000,1000000,-1),(200,500,1000,5000,10000,50000,100000,500000,1000000,-1),(200,500,1000,5000,10000,50000,100000,500000,1000000,-1),(500,5000,50000,500000,-1)),
        'steps' : ((0,5,10,50,250,500,10000,50000,300000,-1),(5,10,50,100,500,1000,10000,50000,500000,-1),(10,50,100,500,1000,5000,25000,150000,500000,-1),(50,500,5000,50000,-1))
    }


    def __select_action(self):
        print('What do you wish to do?\n1. Perform a new search\n2. Present the results from a previous search')
        while True:
            try:
                answer = int(input('Please enter the number of the action: '))
                if answer == 1 or answer == 2: break
                raise Exception
            except KeyboardInterrupt:
                exit()
            except:
                print('Not a valid input. Please try again.')
        return answer


    def __validate_input(self, original, message, boolean, error_message):
        while True:
            try:
                value = input(message)
                if len(value) > 0:
                    if boolean(value): return value
                    raise Exception
                return original
            except KeyboardInterrupt:
                exit()
            except:
                print(f'{error_message} Please try again.')
                continue


    def __define_search(self):
        print('You will now be presented a number of options to define your search. The value inside the parentheses is the default. Press Enter to select the default value, otherwise input your preferred value and press Enter.')

        self.language = self.__validate_input(self.language, f'Language: ({self.language}) ', lambda value: value == 'Java' or value == 'Python', 'Not a valid input.')
        self.computer = int(self.__validate_input(self.computer, f'Computer: ({self.computer}) ', lambda value: int(value) == 1 or int(value) == 2 or int(value) == 3, 'Not a valid input.'))

        # self.min_size = self.__validate_input(self.min_size, f'Minimum size: ({self.min_size}) ', lambda value: int(value) >= 0, 'The value has to be a number and equal to or greater than 0.')
        # self.max_size = self.__validate_input(self.max_size, f'Maximum size: ', lambda value: int(value) > int(self.min_size), 'The value has to be a number and greater than the min value.')
        # self.min_number_of_stars = self.__validate_input(self.min_number_of_stars, f'Minimum number of stars: ({self.min_number_of_stars}) ', lambda value: int(value) >= 0, 'The value has to be a number and equal to or greater than 0.')
        # self.max_number_of_stars = self.__validate_input(self.max_number_of_stars, f'Maximum number of stars: ', lambda value: int(value) > int(self.min_number_of_stars), 'The value has to be a number and greater than the min value.')
        # self.min_number_of_contributors = self.__validate_input(self.min_number_of_contributors, f'Minimum number of contributors: ({self.min_number_of_contributors}) ', lambda value: int(value) >= 0, 'The value has to be a number and equal to or greater than 0.')
        # self.max_number_of_contributors = self.__validate_input(self.max_number_of_contributors, f'Maximum number of contributors: ', lambda value: int(value) > int(self.min_number_of_contributors), 'The value has to be a number and greater than the min value.')


    def __select_search(self):
        db = Database()
        db.connect()

        searches = db.fetch_all('''SELECT * FROM search''')
        print('ID\tDATE\t\tLANGUAGE\tMIN SIZE\tMAX SIZE\tMIN NUMBER OF STARS\tMAX NUMBER OF STARS\tNUMBER OF STARS\t\tMIN NUMBER OF CONTRIBUTORS\tMAX NUMBER OF CONTRIBUTORS')
        search_id_list = []
        for search in searches:
            search_id_list.append(search[0])
            string = str()
            for index in range(0, len(search)):
                value = search[index]
                sep = str()
                match index:
                    case 2:
                        sep = ['\t']*2
                    case 3:
                        sep = ['\t']*2
                    case 4:
                        sep = ['\t']*2
                    case 5:
                        sep = ['\t']*3
                    case 6:
                        sep = ['\t']*3
                    case 7:
                        sep = ['\t']*3
                    case 8:
                        sep = ['\t']*3
                    case _:
                        sep = '\t'
                string += f"{value}{''.join(sep)}"
            print(string)
        while len(self.search_ids) == 0:
            try:
                ids = input('Please enter the IDs of the searches you want to be presented (use a single space as a separator): ').split(' ')
                for id in ids:
                    if int(id) not in search_id_list:
                        raise Exception
                self.search_ids = ids
            except KeyboardInterrupt:
                exit()
            except:
                print('Not a valid input. Please try again.')
        print(f"You've selected the following {'IDs' if len(self.search_ids) > 1 else 'ID'}:", *self.search_ids, sep=' ')

        db.close()

    def __search_low_stars(self):
        """Method to defined fined grained search with size criteria"""
        
        search_ranges = self.Search_java if self.language == 'Java' else self.Search_python
        list = 0
        for stars in search_ranges['stars']:
            start_stars = self.min_number_of_stars if list==0 else search_ranges['stars'][list-1]
            print('Start star : End star ', start_stars , ' : ', search_ranges['stars'][list])
            for i in range(start_stars, stars):
                self.min_size = 100
                self.max_size = self.min_size + search_ranges['steps'][list][0]
                for j in range(0,len(search_ranges['size'][list])):
                    print(search_ranges['size'][list])
                    print(search_ranges['steps'][list])
                    if search_ranges['steps'][list][j] == -1:
                        self.max_size = None
                        print(self.min_size)
                        print(self.max_size)
                        search_id = Search(
                        self.language,
                        self.min_size, self.max_size, # + 1,
                        None, None, i,
                        self.min_number_of_contributors, self.max_number_of_contributors,
                        ).run()
                        Analysis().start_filter(search_id)
                    else:
                        while True:
                            print(self.min_size)
                            print(self.max_size)
                            search_id = Search(
                            self.language,
                            self.min_size, self.max_size, # + 1,
                            None, None, i,
                            self.min_number_of_contributors, self.max_number_of_contributors,
                            ).run()
                            Analysis().start_filter(search_id)
                            input('Press any key')
                            if self.max_size >= search_ranges['size'][list][j]:
                                self.min_size = self.max_size + 1
                                self.max_size = self.min_size + search_ranges['steps'][list][j+1]
                                break
                            else:
                                self.min_size = self.max_size + 1
                                self.max_size = self.min_size + search_ranges['steps'][list][j]
            list += 1

    def run(self):
        """Main method for executing the program."""

        answer = self.__select_action()
        if answer == 1:
            self.__define_search()
            self.max_number_of_stars = 4000 if self.language == 'Java' else 6000
            if self.computer == 1:
                self.min_number_of_stars = 36 if self.language == 'Java' else 66
                for i in range(self.min_number_of_stars, 501):
                    search_id = Search(
                        self.language,
                        self.min_size, self.max_size, # + 1,
                        None, None, i,
                        self.min_number_of_contributors, self.max_number_of_contributors,
                    ).run()
                    # 498 searches
                    Analysis().start_filter(search_id)
            elif self.computer == 3:
                self.__search_low_stars()
            else:
                for i in range(501, 1001):
                    search_id = Search(
                        self.language,
                        self.min_size, self.max_size, # + 1,
                        None, None, i,
                        self.min_number_of_contributors, self.max_number_of_contributors,
                    ).run()
                    # 500 searches
                    Analysis().start_filter(search_id)
                for i in range(1001, self.max_number_of_stars + 1, 100):
                    search_id = Search(
                        self.language,
                        self.min_size, self.max_size, # + 1,
                        i, None if i + 100 > self.max_number_of_stars else i + 100, None,
                        self.min_number_of_contributors, self.max_number_of_contributors,
                    ).run()
                    # 30 or 50 searches
                    Analysis().start_filter(search_id)
        else:
            self.__select_search()
            results = Results(self.search_ids)
            results.print_to_screen()
            results.write_to_file()


if __name__ == '__main__':
    Main().run()
