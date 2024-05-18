import csv
from pathlib import Path
from datetime import datetime
from datetime import date
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import scipy as sp
import numpy as np 
from scipy.stats import ttest_ind
from scipy.stats import tukey_hsd
import statsmodels.api as sm
from database.database import Database


class Results:
    """Responsible for presenting the results."""

    __RESULT_PARAMETERS = ['stars', 'size', 'contributors']


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
        sqliv_category_res_java = self.__get_variable_plot_data(results[7])
        sqliv_category_res_python = self.__get_variable_plot_data(results[8])
        repos_with_sqliv = len(count_sqliv_in_repos)
        count_analyzed_repos = count_repos_with_no_sqliv + repos_with_sqliv
        print('------Results From Analysis-----')
        self.__print_basics(count_sqliv_in_repos, count_repos_with_no_sqliv,count_searched_repos, count_sqliv_by_language, count_no_sqliv_by_language,count_analyzed_repos,sqliv_type_results_java,sqliv_type_results_python)
        self.__do_stats('size',sqliv_category_res_python[2],sqliv_category_res_python[3],sqliv_category_res_java[2],sqliv_category_res_java[3])
        self.__do_stats('contributors',sqliv_category_res_python[4],sqliv_category_res_python[5],sqliv_category_res_java[4],sqliv_category_res_java[5])
        self.__do_stats('date',sqliv_category_res_python[6],sqliv_category_res_python[7],sqliv_category_res_java[6],sqliv_category_res_java[7])
        self.__plot_boxplot(sqliv_category_res_python[2],sqliv_category_res_python[3],sqliv_category_res_java[2],sqliv_category_res_java[3], 'size (kb)', 'upper right', 100, 200000)
        self.__plot_boxplot(sqliv_category_res_python[4],sqliv_category_res_python[5],sqliv_category_res_java[4],sqliv_category_res_java[5], 'contributors', 'upper right', 2, 20)
        self.__plot_boxplot(sqliv_category_res_python[6],sqliv_category_res_python[7],sqliv_category_res_java[6],sqliv_category_res_java[7], 'date', 'lower right', dates=True)      
        

    def __print_basics(self, count_sqliv_in_repos, count_repos_with_no_sqliv, count_searched_repos, count_sqliv_by_language, count_no_sqliv_by_language, count_analyzed_repos, sqliv_type_results_java, sqliv_type_results_python):
        """Print result"""
        print(f'{"Searches included in result compilation:":<40}', self.__searchID)
        print(f'{"Total number of repos in search:":<40}', count_searched_repos)
        print(f'{"Total number of analyzed repos:":<40}', count_analyzed_repos)
        if count_analyzed_repos > 0:
            total = sqliv_type_results_java['concat'] + sqliv_type_results_java['prep_concat'] + sqliv_type_results_python['concat'] + sqliv_type_results_python['prep_concat']
            print(f'{"Total number of repos with SQLiv:s":<40}',  total, '(', (total/count_analyzed_repos)*100, '%)')
        print(f'{"Analyzed repos without SQLiv:s found":<40}', count_repos_with_no_sqliv + sqliv_type_results_java['prep']+sqliv_type_results_python['prep'])
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
        print(count_no_sqliv_by_language)
        print('')
        for res in count_no_sqliv_by_language:
            print(f'{res[0]}{" repos without concatenated and/or prepared statements":<40}', res[1])

    def __get_variable_plot_data(self, sqliv_type_results):
        """Split results for category scatter plots"""
        def __append_res(current, prep_concat : bool):
            if prep_concat:
                for list in xlist:
                    list.append('prepared and concatenation')
            elif current[5] == None:
                for list in xlist:
                    list.append('hard coded')
            else:    
                for list in xlist:
                    list.append(current[5])
            if current[1] == None: #stars
                stars_x.pop()
            else:
                stars_y.append(current[1])
            if current[2] == None: #size
                size_x.pop()
            else:
                size_y.append(current[2])
            if current[3] == None: #contributors
                contributors_x.pop()
            else:
                contributors_y.append(current[3])
            if current[6] == None or current[6] =='no date': #Updated at
                updated_x.pop()
            else:
                updated_y.append(datetime.strptime(current[6],'%Y-%m-%d').toordinal())
                
        stars_x = []
        stars_y = []
        size_x = []
        size_y = []
        contributors_x = []
        contributors_y = []
        updated_x = []
        updated_y = []
        xlist = [stars_x, size_x, contributors_x, updated_x]
        result_length = len(sqliv_type_results)
        index = 0
        if result_length > 0:
            while True:
                current = sqliv_type_results[index]
                if index >= result_length-1:
                    __append_res(current, False)
                    break
                index += 1
                next = sqliv_type_results[index]
                if current[0] == next[0]:
                    __append_res(current, True)
                    index += 1
                else:
                    __append_res(current, False)
                if index > result_length-1:
                    break
        return [stars_x, stars_y, size_x, size_y, contributors_x,  contributors_y, updated_x, updated_y]


    def __get_sqliv_type_results(self, sqliv_type_results) -> dict:
        """Split results for type of sqliv"""
        
        Type_count = {'prep':0,'concat':0,'prep_concat':0}
        result_length = len(sqliv_type_results)
        index = 0
        if result_length > 0:
            while True:
                current = sqliv_type_results[index]
                if current[5] == None:
                    index += 1
                    break
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
    

    def __do_stats(self, metric, results_x_p : list, results_y_p: list, results_x_j: list, results_y_j: list):
        """Function to calculate and present statistics for the data.
        t-test for comparison of categories between languages and tuckey HSD to compare between categories in one language.
        CDF is also calculated and plotted for each metric.
        """
        Category_P = {'prep':[], 'concat':[], 'hard coded':[], 'prepared and concatenation':[]}
        Category_J = {'prep':[], 'concat':[], 'hard coded':[], 'prepared and concatenation':[]}
        for i,item in enumerate(results_x_p):
            Category_P[item].append(results_y_p[i])
        for i,item in enumerate(results_x_j):
            Category_J[item].append(results_y_j[i])
        if len(results_y_p) > 0 and len(results_y_j) > 0:
            print(f'T-test for categories on metric {metric} comparing between java and python')
            if len(Category_J['prep']) > 0 and len(Category_P['prep']) > 0:
                print('T-test for prep: ', ttest_ind(Category_J['prep'], Category_P['prep']))
            if len(Category_J['concat']) > 0 and len(Category_P['concat']) > 0:
                print('T-test for concat: ', ttest_ind(Category_J['concat'], Category_P['concat']))
            if len(Category_J['hard coded']) > 0 and len(Category_P['hard coded']) > 0:
                print('T-test for hard coded: ', ttest_ind(Category_J['hard coded'], Category_P['hard coded']))     
            if len(Category_J['prepared and concatenation']) > 0 and len(Category_P['prepared and concatenation']) > 0: 
                print('T-test for prepared and concatenation: ', ttest_ind(Category_J['prepared and concatenation'], Category_P['prepared and concatenation']))
        else:
            print('Only one language in results. No comparison statistics between languages calculated')
        
        print(f'Tukey HSD for {metric}')
        java_args = []
        python_args = []
        for k,v in Category_J.items():
            if len(v) > 0:
                java_args.append(Category_J[k])
        for k,v in Category_P.items():
            if len(v) > 0:
                python_args.append(Category_P[k])

        if len(java_args) > 1:
            tj = tukey_hsd(*java_args)
            print('tuckey for java projects:\n', tj)
            print('exact p-values java\n',getattr(tj,'pvalue'))
        else:
            print('No sql categories to compare in java projects')
        if len(python_args) > 1:
            tp = tukey_hsd(*python_args)
            print('tuckey for python projects:\n', tp)
            print('exact p-values python\n',getattr(tp,'pvalue'))
        else:
            print('No sql categories to compare in python projects')

        f, ax = plt.subplots()
        countj, bins_countj = np.histogram(Category_J['hard coded']+Category_J['prepared and concatenation']+Category_J['concat']+Category_J['prep'], bins=75)
        pdfj = countj / sum(countj) 
        cdfj = np.cumsum(pdfj) 
        plt.plot(bins_countj[1:], cdfj, '#fdafaf', label=f"CDF {metric} java")
        countp, bins_countp = np.histogram(Category_P['hard coded']+Category_P['prepared and concatenation'] + Category_P['concat'] + Category_P['prep'], bins=75)
        pdfp = countp / sum(countp) 
        cdfp = np.cumsum(pdfp) 
        plt.plot(bins_countp[1:], cdfp, '#B1B1FF', label=f"CDF {metric} python")
        plt.title(f'Cumulative distribution for {metric}', fontsize=20)
        ax.set_xlabel(metric)
        if metric=='date':
            new_labels = []
            for item in ax.get_xticks():
                new_labels.append(date.fromordinal(int(item)))
            ax.set(xticklabels=new_labels)
            ax.set_xlabel('Latest update')
            plt.title(f'Cumulative distribution for latest update', fontsize=20)
            plt.xticks(rotation=10)
        plt.legend()
        plt.setp(ax.get_legend().get_texts(), fontsize='11') # for legend text
        plt.setp(ax.get_legend().get_title(), fontsize='13') # for legend title
        plt.show()      

    def __plot_boxplot(self, results_x_p, results_y_p, results_x_j, results_y_j, metric, legend, y_min = None, y_max = None, dates = False):
            lang_python = []
            lang_java = []
            for item in results_y_p:
                lang_python.append('python')
            for item in results_y_j:
                lang_java.append('java')

            cat_x = results_x_j + results_x_p 
            metric_y = results_y_j + results_y_p
            size_lang = lang_java + lang_python
            size_data = {'SQL category': cat_x,  'language': size_lang}
            size_data[metric] = metric_y
            
            f, ax = plt.subplots()
            plt.title(f'SQL category vs {metric}', fontsize=25)
            plt.xticks(rotation=10)
            sns.boxplot(size_data, x='SQL category', y=f'{metric}', hue='language', order=['hard coded', 'prepared and concatenation', 'concat', 'prep'], palette={"java": "#fdafaf", "python": "#B1B1FF"})
            if y_min or y_max:
                ax.set_ylim(y_min, y_max)
            ax.set_xlabel('SQL category', fontsize=15)
            ax.set_ylabel(f'{metric}', fontsize=15)
            sns.move_legend(ax, f'{legend}', title='Language')
            plt.setp(ax.get_legend().get_texts(), fontsize='11') # for legend text
            plt.setp(ax.get_legend().get_title(), fontsize='13') # for legend title
            if dates:
                new_labels = []
                for item in ax.get_yticks():
                    new_labels.append(date.fromordinal(int(item)))
                ax.set(yticklabels=new_labels)
            plt.show()

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
        get_sqliv_categories_java = DB.fetch_all(f'''SELECT r.repository, repo.number_of_stars, repo.size, repo.number_of_contributors, r.sqliv, st.type, repo.updated_at, Count(*) from result r
                    LEFT JOIN sqliv st on r.id=st.result
                    LEFT JOIN search s on s.id=r.search
                    LEFT JOIN language l on s.language=l.id
					LEFT JOIN repository repo on repo.id = r.repository
		            WHERE search IN ({','.join(['?']*len(self.__searchID))}) AND l.id=1
		            GROUP BY r.repository, st.type
		            ORDER BY r.sqliv ASC, r.repository ASC''', self.__searchID)
        get_sqliv_categories_python = DB.fetch_all(f'''SELECT r.repository, repo.number_of_stars, repo.size, repo.number_of_contributors, r.sqliv, st.type, repo.updated_at, Count(*) from result r
                    LEFT JOIN sqliv st on r.id=st.result
                    LEFT JOIN search s on s.id=r.search
                    LEFT JOIN language l on s.language=l.id
					LEFT JOIN repository repo on repo.id = r.repository
		            WHERE search IN ({','.join(['?']*len(self.__searchID))}) AND l.id=2
		            GROUP BY r.repository, st.type
		            ORDER BY r.sqliv ASC, r.repository ASC''', self.__searchID)
        count_searched_repos = DB.fetch_one(f'''SELECT COUNT(*) from search_repository WHERE search IN ({','.join(['?']*len(self.__searchID))})''', self.__searchID)[0]
        DB.close()
        return [count_sqliv_in_repos, count_sqliv_by_language, count_repos_with_no_sqliv, count_no_sqliv_by_language, count_searched_repos, get_sqliv_type_java, get_sqliv_type_python, get_sqliv_categories_java, get_sqliv_categories_python]
    
if __name__ == '__main__':
    r = Results((3,4))
    r.print_to_screen()
    r.write_to_file()