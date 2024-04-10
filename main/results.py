import csv
from datetime import datetime
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy as sp
from database.database import Database


class Results:
    """Responsible for presenting the results."""

    __RESULT_PARAMETERS = ['stars', 'followers', 'size', 'contributors']


    def __init__(self, searchID : tuple):
        """The constructor..."""
        self.__searchID = searchID


    def print_to_screen(self):
        """Print results to screen"""
        DB = Database()
        DB.connect()
        results = self.__get_raw_results()
        count_sqliv_in_repos = results[0]
        count_sqliv_by_language = results[1]
        count_repos_with_no_sqliv = results[2]
        count_no_sqliv_by_language = results[3]
        count_searched_repos = results[4]
        sqliv_type_results_java = self.__get_sqliv_type_results(results[5])
        sqliv_type_results_python = self.__get_sqliv_type_results(results[6])
        repos_with_sqliv = len(count_sqliv_in_repos)
        count_analyzed_repos = count_repos_with_no_sqliv + repos_with_sqliv

        print('------Results From Analysis-----')
        self.__print_basics(count_sqliv_in_repos, count_repos_with_no_sqliv, count_searched_repos, count_sqliv_by_language, count_no_sqliv_by_language, count_analyzed_repos, sqliv_type_results_java, sqliv_type_results_python)
        #Start printing plots
        fig, (stars, size) = plt.subplots(2)
        fig.suptitle('Number of found SQLivs in project vs')
        self.__sort_and_print(count_sqliv_in_repos, 1, stars)
        self.__sort_and_print(count_sqliv_in_repos, 2, size)
        plt.tight_layout()
        plt.draw()
        plt.show()


    def __sort_and_print(self, repo_sqliv_stats : list, result_parameter : int, axel):
         """Sort found sqliv by result parameter and plot figure subplot"""
         x = []
         y = []
         for val in repo_sqliv_stats:
              x.append(val[result_parameter])
              y.append(val[4])
         axel.set_title(self.__RESULT_PARAMETERS[result_parameter-1])
         axel.set(ylabel='SQLIV in repo', xlabel=f'{self.__RESULT_PARAMETERS[result_parameter-1]} in repo')
         axel.plot(x, y, 'o', color='black')


    def __print_basics(self, count_sqliv_in_repos, count_repos_with_no_sqliv, count_searched_repos, count_sqliv_by_language, count_no_sqliv_by_language, count_analyzed_repos, sqliv_type_results_java, sqliv_type_results_python):
        """Print result"""
        print(f'{"Searches included in result compilation:":<40}', self.__searchID)
        print(f'{"Total number of repos in search:":<40}', count_searched_repos)
        print(f'{"Total number of analyzed repos:":<40}', count_analyzed_repos)
        if count_analyzed_repos > 0:
            total = sqliv_type_results_java['concat'] + sqliv_type_results_java['prep_concat'] + sqliv_type_results_python['concat'] + sqliv_type_results_python['prep_concat']
            print(f'{"Total number of repos with SQLiv:s":<40}',  total, '(', (total/count_analyzed_repos)*100, '%)')
        print(f'{"Analyzed repos without SQLiv:s found":<40}', count_repos_with_no_sqliv + sqliv_type_results_java['prep'])
        for res in count_sqliv_by_language:
            print(f'{res[0]}{" repos with concatenated and/or prepared statements":<40}', res[1])
        print('')
        print('Java figures concatenated and/or prepared statements')
        print(f'{sqliv_type_results_java["prep_concat"]}{" repos with concatenation and prepared statements."}')
        print(f'{sqliv_type_results_java["concat"]}{" repos with concatenation only."}')
        print(f'{sqliv_type_results_java["prep"]}{" repos with prepared statements only."}')
        print('Python figures concatenated and/or prepared statements')
        print(f'{sqliv_type_results_python["prep_concat"]}{" repos with concatenation and prepared statements."}')
        print(f'{sqliv_type_results_python["concat"]}{" repos with concatenation only."}')
        print(f'{sqliv_type_results_python["prep"]}{" repos with prepared statements only."}')
        print('')
        for res in count_no_sqliv_by_language:
            print(f'{res[0]}{" repos without concatenated and/or prepared statements":<40}', res[1])




    def __get_sqliv_type_results(self, sqliv_type_results) -> dict:
        """Split results for type of sqliv"""
        
        Type_count = {'prep':0,'concat':0,'prep_concat':0}
        result_length = len(sqliv_type_results)
        index = 0
        if result_length > 0:
            while True:
                current = sqliv_type_results[index]
                if index >= result_length-1:
                    Type_count[current[5]] += 1
                    break
                index += 1
                next = sqliv_type_results[index]
                if current[0] == next[0]:
                    Type_count['prep_concat'] += 1
                    index += 1
                else:
                    Type_count[current[5]] += 1
                if index > result_length-1:
                    break
        return Type_count
            

    def write_to_file(self):
        """Write results to file"""
        DB = Database()
        DB.connect()
        results = self.__get_raw_results()
        count_sqliv_in_repos = results[0]
        count_sqliv_by_language = results[1]
        count_repos_with_no_sqliv = results[2]
        count_no_sqliv_by_language = results[3]
        count_searched_repos = results[4]
        sqliv_type_results_java = self.__get_sqliv_type_results(results[5])
        sqliv_type_results_python = self.__get_sqliv_type_results(results[6])
        repos_with_sqliv = len(count_sqliv_in_repos)
        count_analyzed_repos = count_repos_with_no_sqliv + repos_with_sqliv
        raw_results =DB.fetch_all(f'''SELECT search, repository, sqliv, r.number_of_stars, size, number_of_contributors, st.file_relative_repo, st.location from result r
                    LEFT JOIN sqliv st ON r.id=st.result
                    LEFT JOIN search s on s.id=r.search
                    LEFT JOIN language l on s.language=l.id
                    WHERE search IN ({','.join(['?']*len(self.__searchID))})
                    ORDER BY sqliv DESC,
                    repository ASC''', self.__searchID)
        now = datetime.now()
        current_time = now.strftime('%d_%m_%Y-%H_%M_%S')
        output = f'resultCSV{current_time}.csv'
        with open(output, 'w', newline='') as file:
            writer=csv.writer(file)
            ids = ['Search id included in results']
            for id in self.__searchID:
                ids.append(id)
            writer.writerow(ids)
            writer.writerow(['Number of repos searched', count_searched_repos])
            writer.writerow(['Number of repos analyzed', count_analyzed_repos])
            writer.writerow(['Number of repos with found SQLIV', sqliv_type_results_java['concat'] + sqliv_type_results_java['prep_concat'] + sqliv_type_results_python['concat'] + sqliv_type_results_python['prep_concat']])
            writer.writerow(['Number of repos without found SQLIV', count_repos_with_no_sqliv + sqliv_type_results_java['prep']+sqliv_type_results_python['prep']])
            writer.writerow(['Start of found SQLIV by language in analyzed repos'])
            writer.writerows([['java', sqliv_type_results_java['concat'] + sqliv_type_results_java['prep_concat']],['python', sqliv_type_results_python['concat'] + sqliv_type_results_python['prep_concat']]])
            writer.writerow(['Start of no SQLIV by language in analyzed repos'])
            writer.writerows(count_no_sqliv_by_language)
            writer.writerow(['Start of repos with concat, prepared or prepared+concat'])
            writer.writerow(['Repo id', 'stars', 'size',  'contributors', 'sqliv', 'type', 'number of found SQLIV'])
            writer.writerows(results[5])
            writer.writerows(results[6])
            writer.writerow(['Start of raw results'])
            writer.writerow(['Search id', 'Repo id', 'SQLIV', 'stars', 'size', 'contributors', 'file', 'location'])
            for i in range(0,len(raw_results)):
                try:
                    writer.writerow(raw_results[i])
                except UnicodeEncodeError:
                    raw_results[i][6] = 'Encoding error'
                    writer.writerow(raw_results[i])



    def __get_raw_results(self):
        """Collect data from data base for result presentation"""
        DB = Database()
        DB.connect()
        count_sqliv_in_repos = DB.fetch_all(f'''SELECT repository, s.number_of_stars, size, number_of_contributors, COUNT(*) from result r
                    LEFT JOIN sqliv st on r.id=st.result
                    LEFT JOIN search s on s.id=r.search
                    LEFT JOIN language l on s.language=l.id
                    WHERE search IN ({','.join(['?']*len(self.__searchID))})
                    AND sqliv=1
                    GROUP BY r.repository
                    ''', self.__searchID)
        count_sqliv_by_language = DB.fetch_all(f'''SELECT l.name, COUNT(*) from result r
                    LEFT JOIN search s on s.id=r.search
                    LEFT JOIN language l on s.language=l.id
                    WHERE search IN ({','.join(['?']*len(self.__searchID))})
                    AND sqliv=1
                    GROUP BY l.name''', self.__searchID)
        count_repos_with_no_sqliv = DB.fetch_one(f'''SELECT COUNT(*) from result r
                    WHERE search IN ({','.join(['?']*len(self.__searchID))})
                    AND sqliv=0
                    ''', self.__searchID)[0]
        count_no_sqliv_by_language = DB.fetch_all(f'''SELECT l.name, COUNT(*) from result r
                    LEFT JOIN search s on s.id=r.search
                    LEFT JOIN language l on s.language=l.id
                    WHERE search IN ({','.join(['?']*len(self.__searchID))})
                    AND sqliv=0
                    GROUP BY l.name''', self.__searchID)
        get_sqliv_type_java = DB.fetch_all(f'''SELECT repository, s.number_of_stars, size, number_of_contributors, r.sqliv, st.type, Count(*) from result r
                    LEFT JOIN sqliv st on r.id=st.result
                    LEFT JOIN search s on s.id=r.search
                    LEFT JOIN language l on s.language=l.id
		            WHERE r.sqliv = 1 AND search IN ({','.join(['?']*len(self.__searchID))}) AND l.id=1
		            GROUP BY r.repository, st.type
		            ORDER BY r.sqliv ASC, r.repository ASC''', self.__searchID)
        get_sqliv_type_python = DB.fetch_all(f'''SELECT repository, s.number_of_stars, size, number_of_contributors, r.sqliv, st.type, Count(*) from result r
                    LEFT JOIN sqliv st on r.id=st.result
                    LEFT JOIN search s on s.id=r.search
                    LEFT JOIN language l on s.language=l.id
		            WHERE r.sqliv = 1 AND search IN ({','.join(['?']*len(self.__searchID))}) AND l.id=2
		            GROUP BY r.repository, st.type
		            ORDER BY r.sqliv ASC, r.repository ASC''', self.__searchID)
        count_searched_repos = DB.fetch_one(f'''SELECT COUNT(*) from search_repository WHERE search IN ({','.join(['?']*len(self.__searchID))})''', self.__searchID)[0]
        DB.close()
        return [count_sqliv_in_repos, count_sqliv_by_language, count_repos_with_no_sqliv, count_no_sqliv_by_language, count_searched_repos, get_sqliv_type_java, get_sqliv_type_python]
    
if __name__ == '__main__':
    r = Results((3,4))
    r.print_to_screen()
    r.write_to_file()