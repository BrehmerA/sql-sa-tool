import os
import shutil
import stat
import sys
import runAnalysis
from multiprocessing import Pool
from pathlib import Path
sys.path.append(os.path.dirname(os.path.abspath(__file__))) # Appends the parent dir to the python path.
from database.database import Database


class Analysis:
    """Responsible for analyzing the selected repositories.

    The source code of each repository will be searched for SQLIVs.
    """

    DB = Database()

    def __init__(self):
        """The constructor..."""
        if not os.path.exists(os.getcwd()+'/cloned'):
            os.mkdir(os.getcwd+'/cloned')
        self.DB.connect()
    
    def startFilter(self, searchID) -> dict:
        self.__searchForDBConnections("Python", searchID)
        #self.__searchForDBConnections("Java", searchID)
        

    def __searchForDBConnections(self, lang, searchID):
        """Search found repositories for DB operations"""
        path = self.__prepareFolder(lang, searchID)
        repos = self.__getRepos(lang, searchID)
        var = [(lang, path, rep) for rep in repos]
        print(var)
        print("Analyserar: " + str(len(repos)) + " repos")
        
        with Pool() as p:
            p.starmap(runAnalysis.search, var)

    def __getRepos(self, lang, searchID) -> list:
        """Get repos from DB after search"""

        dbResults = self.DB.fetch_all('''SELECT DISTINCT url
                                    FROM search_repository sr
                                    LEFT JOIN repository r 
                                    ON r.id = sr.repository
                                    LEFT JOIN search s
                                    ON s.id = sr.search
                                    LEFT JOIN language l
                                    ON s.language = l.id
                                    WHERE sr.search = ?
                                    AND l.name = ?
                                    AND r.number_of_stars < ?
                                 ''',(searchID, lang, 5700)) #Number of stars to reduce repos for testing purpose
        urls = [url[0] for url in dbResults]
        html_urls = []
        for url in urls:
            split = url.split('/')
            html_urls.append('https://github.com/' + split[-2]+'/'+split[-1]+'.git')
        return html_urls   

    def __prepareFolder(self, lang, searchID) -> str:
        """
            Prepare the folder structure to receive and analyse projects.
        """
        basePath = os.getcwd()+'/cloned'
        existingFolders = len(os.listdir(basePath))
        path = basePath+'/'+str(searchID)+lang+str(existingFolders)
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
                    print("Could not empty folder")
        else:
            os.makedirs(path)
        return path
            

if __name__ == '__main__':
    a = Analysis()
    a.startFilter(2)