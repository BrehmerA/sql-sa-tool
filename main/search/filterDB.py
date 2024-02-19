from html import unescape
from pathlib import Path
from ghapi.all import GhApi
import os
import subprocess
import re
import ntpath
import shutil

class FilterDB:
    """Responsible for filtering list of repositories on projects containing DB drivers.
        Will work for projects written in Java and Python.
    """

    #Class variables
    DBDriverJavaObjectFunction = ['Statement','ResultSet','PreparedStatement','TypedQuery']
    DBDriverPythonImports = ["pymssql", "asyncpg", "pyodbc", "sqlite3"]
    PATH_TO_TOKEN = Path(__file__).resolve().parent / '.token'
    token = None
    api = None

    def __init__(self):
        """Init"""
        # TODO: check that cloned to folder exist and is empty.
        self.toAnalyse = {
            "python" : [],
            "java" : []
        }
        
    def startFilter(self) -> dict:
        self.searchForDBConnections("python")
        #self.searchForDBConnections("java")
        return self.toAnalyse

    def searchForDBConnections(self, lang):
        """Search found repositories for DB operations"""
        repos = self.getRepos(lang)
        path = os.getcwd()
        for repo in repos:
            baseName = ntpath.basename(repo)[:-4]
            cloneInto = Path(path+'/cloned/' + baseName)
            complete = subprocess.run(["git", "clone", "--depth","1", repo , cloneInto])
            if self.searchFiles(complete, lang):
                self.toAnalyse[lang].append(cloneInto)
            else:
                print("DELETE")
                # TODO: Safe delete not used repos.

    def getRepos(self, lang) -> list:
        """Get repos from DB after search"""
        # TODO: Collect results from DB instead of test list.
        if(lang=="python"):
            return ["https://github.com/omnilib/aiosqlite.git", "https://github.com/techouse/mysql-to-sqlite3.git","https://github.com/BrehmerA/sql-repo-tester.git"]
        elif(lang=="java"):
            return ["https://github.com/dbeaver/dbeaver.git", "https://github.com/opensearch-project/sql.git","https://github.com/BrehmerA/sql-repo-tester.git"]
        else:
            raise TypeError("Non legal language chosen for DB driver search")

    def searchFiles(self,complete, lang) -> bool:
        """Search cloned repos for db drivers. Search all files in repo with lang extension stop search for separate files at first find."""
        dirPath = complete.args[5]
        extension = ""
        searchRegex = ""
        if (lang=="python"):
            extension = "*.py"
            searchRegex = self.createSearchRegexPython()
        elif(lang=="java"):
            extension = "*.java"
            searchRegex = self.createSearchRegexJava()
        for file in list(dirPath.rglob(extension)):
            with open(file, 'r') as fp:
                for line in fp:
                    if(re.search(searchRegex, line)):
                        return True
        return False  

    def searchLines(self, file, searchRegex):
        """Search single file for db driver"""
       

    def createSearchRegexJava(self) -> str:
        """Define the search regex for the java DB driver"""
        classNames = ""
        for c in self.DBDriverJavaObjectFunction:
            classNames = classNames + c + "|"
        regex = r'^(?=.*\b('+classNames+r')\b).*$'
        return regex

    def createSearchRegexPython(self) -> str:
        """Define the search regex for the python DB drivers"""
        drivers = ""
        for driver in self.DBDriverPythonImports:
            drivers = drivers + driver + "|"
        drivers = drivers[:-1]
        regex = r'^(?=.*\b(import)\b)(?=.*\b('+drivers+r')\b).*$'
        return regex
    

if __name__ == '__main__':
    search = FilterDB()
    print(search.startFilter())
