import os
import shutil
import stat
import sys
from multiprocessing import Pool
from pathlib import Path

import runAnalysis
from database.database import Database


class Analysis:
    """Responsible for analyzing the selected repositories.
    The source code of each repository will be searched for SQLIVs.
    """

    DB = Database()


    def __init__(self):
        """The constructor..."""
        if not os.path.exists(os.getcwd() + '/cloned'):
            os.mkdir(os.getcwd() + '/cloned')


    def startFilter(self, searchID) -> dict:
        """Start the filtering and analysis"""
        self.__searchForDBConnections("Python", searchID)
        self.__searchForDBConnections("Java", searchID)


    def __searchForDBConnections(self, lang, searchID):
        """Search found repositories for DB operations."""

        path = self.__prepareFolder(lang, searchID)
        repos = self.__getRepos(lang, searchID)
        var = [(lang, path, rep[0], rep[1], searchID) for rep in repos]
        var_length = len(var)
        batch = 20
        print(f'Analyzing {str(len(repos))} repos.')
        for i in range(0, var_length, batch):
            if i+batch < var_length:
                nextBatch = [var[index] for index in range(i,i+batch)]
            else:
                nextBatch = [var[index] for index in range(i,var_length)]
            with Pool(4) as p:
                p.starmap(runAnalysis.search, nextBatch)
            self.__checkCleanUp(path)

    def __getRepos(self, lang, searchID) -> list:
        """Get repos from DB after search"""

        self.DB.connect()
        dbResults = self.DB.fetch_all(
            '''SELECT DISTINCT url, repository
            FROM search_repository sr
            LEFT JOIN repository r
            ON r.id = sr.repository
            LEFT JOIN search s
            ON s.id = sr.search
            LEFT JOIN language l
            ON s.language = l.id
            WHERE sr.search = ?
            AND l.name = ?
            ''', (searchID, lang))
        repos = []
        for url in dbResults:
            temp = []
            split = url[0].split('/')
            temp.append('https://github.com/' + split[-2]+ '/' +split[-1] + '.git')
            temp.append(url[1])
            repos.append(temp)
        self.DB.close()
        return repos


    def __prepareFolder(self, lang, searchID) -> str:
        """Prepare the folder structure to receive and analyse projects."""

        basePath = os.getcwd() + '/cloned'
        existingFolders = len(os.listdir(basePath))
        path = basePath + '/' + str(searchID) + lang + str(existingFolders)
        if os.path.exists(path) and not os.path.isfile(path):
            if len(os.listdir(path)) != 0:
                for root, dirs, files in os.walk(path):
                    for dir in dirs:
                        os.chmod(os.path.join(root, dir), stat.S_IRWXU)
                    for file in files:
                        os.chmod(os.path.join(root, file), stat.S_IRWXU)
                try:
                    shutil.rmtree(path)
                except:
                    print('Could not empty folder.')
        else:
            os.makedirs(path)
        return path
    
    def __checkCleanUp(self, path):
        """Function to clean up in a folder and sub folders"""
        if os.path.exists(path) and not os.path.isfile(path):
            if len(os.listdir(path)) != 0:
                for root, dirs, files in os.walk(path):
                    for dir in dirs:
                        os.chmod(os.path.join(root, dir), stat.S_IRWXU)
                    for file in files:
                        os.chmod(os.path.join(root, file), stat.S_IRWXU)
                try:
                    shutil.rmtree(path)
                except:
                    print('Could not empty folder.')

if __name__=='__main__':
    pass