import os
import subprocess
import ntpath
import shutil
import stat
import re
from pathlib import Path


DBDriverJavaObjectFunction = ['Statement','ResultSet','PreparedStatement','TypedQuery']
DBDriverPythonImports = ["pymssql", "asyncpg", "pyodbc", "sqlite3"]

def search(lang, path, repo):   
    baseName = ntpath.basename(repo)[:-4]
    cloneInto = Path(path + '/' + baseName)
    complete = subprocess.run(["git", "clone", "--depth","1", repo , cloneInto], 
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.STDOUT)
    if __searchFiles(complete, lang):
        __performSQLIVAnalysis(cloneInto)

    for root, dirs, files in os.walk(cloneInto):  
        for dir in dirs:
            os.chmod(os.path.join(root, dir), stat.S_IRWXU)
        for file in files:
            os.chmod(os.path.join(root, file), stat.S_IRWXU)
    try:
        shutil.rmtree(cloneInto)
    except:
        print("Problem deleting file in ")

def __searchFiles(complete, lang) -> bool:
        """Search cloned repos for db drivers. Search all files in repo with lang extension stop search for repo at first find."""
        dirPath = complete.args[5]
        extension = ""
        searchRegex = ""
        found = False
        if (lang=="Python"):
            extension = "*.py"
            searchRegex = __createSearchRegexPython()
        elif(lang=="Java"):
            extension = "*.java"
            searchRegex = __createSearchRegexJava()
        for file in list(dirPath.rglob(extension)):
            try:
                f=open(file)
            except FileNotFoundError:
                print('File not found')
            except PermissionError:
                print('No permission to open file')
            except:
                print('Unknown error')
            else:
                with f as fp:
                    try:
                        for line in fp:
                            if(re.search(searchRegex, line)):
                                found = True
                                return found
                    except Exception as e:
                        print("Could not read file")
        return found

def __createSearchRegexJava() -> str:
    """Define the search regex for the java DB driver"""
    classNames = ""
    for c in DBDriverJavaObjectFunction:
        classNames = classNames + c + "|"
    regex = r'^(?=.*\b('+classNames+r')\b).*$'
    return regex

def __createSearchRegexPython() -> str:
    """Define the search regex for the python DB drivers"""
    drivers = ""
    for driver in DBDriverPythonImports:
        drivers = drivers + driver + "|"
    drivers = drivers[:-1]
    regex = r'^(?=.*\b(import)\b)(?=.*\b('+drivers+r')\b).*$'
    return regex

def __performSQLIVAnalysis(cloneInto):
    print("Performing SQLIV analysis on: " + str(cloneInto))