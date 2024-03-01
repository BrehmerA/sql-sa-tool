import os
import subprocess
import ntpath
import shutil
import stat
import re
import csv
import sys
from pathlib import Path
sys.path.append(os.path.dirname(os.path.abspath(__file__))) # Appends the parent dir to the python path.
from database.database import Database


DBDriverJavaObjectFunction = ['Statement','ResultSet','PreparedStatement','TypedQuery']
DBDriverPythonImports = ["pymssql", "asyncpg", "pyodbc", "sqlite3", "mysql.connector"]
codeQLDB = 'codeQLDBmap'


def search(lang, path, repo, repoID, searchID):   
    baseName = ntpath.basename(repo)[:-4]
    cloneInto = Path(path + '/' + baseName)
    complete = subprocess.run(["git", "clone", "--depth","1", repo , cloneInto], 
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.STDOUT)
    if __searchFiles(complete, lang):
        analysisResults = __performSQLIVAnalysis(cloneInto, lang)
        __saveAnalysisResults(analysisResults, repoID, searchID)
    else:
        print("No sql found on " + str(cloneInto))
    try:
        for root, dirs, files in os.walk(cloneInto):  
            for dir in dirs:
                os.chmod(os.path.join(root, dir), stat.S_IRWXU)
            for file in files:
                os.chmod(os.path.join(root, file), stat.S_IRWXU)
    
        shutil.rmtree(cloneInto)
    except Exception as e:
        print("Problem deleting file in " + str(cloneInto))
        print(e)

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
                        pass
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

def __performSQLIVAnalysis(cloneInto : Path, lang: str) -> dict:
    """Perform the codeQL analysis and save results to DB"""
    resultDict = {
        "sqliv" : None,
        "type" : [],
    }
    packs = 'python-security-extended.qls' if lang=='Python' else 'java-security-extended.qls'
    lookFor = 'SQL query built from user-controlled sources' if lang=='Python' else 'Query built by concatenation with a possibly-untrusted string'
    codeQLDir = Path(os.path.abspath(__file__)).parent.parent.joinpath('codeql/codeql').absolute()
    language = f'--language={str(lang).lower()}'
    source = f'--source-root={cloneInto}'
    newDBpath = Path.joinpath(cloneInto, Path(codeQLDB))
    output = f'--output={cloneInto}\\resCodeScanCSV.csv'
    outputFile = f'{cloneInto}\\resCodeScanCSV.csv'
    print("Start analysis for " + str(cloneInto))
    completeBuild = subprocess.Popen([str(codeQLDir), "database", "create", str(newDBpath), source, language], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) # Create the analysis database
    cmdBuildOutput = completeBuild.stdout.read().decode('utf-8')
    if 'Successfully created database' in cmdBuildOutput:
        print("Running analysis on " + str(cloneInto))
        completeAnalysis = subprocess.run([str(codeQLDir), "database", "analyze", str(newDBpath), packs, "--format=CSV", output], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        print(completeAnalysis)
        try:
            with open(outputFile) as results:
                    reader = csv.reader(results, delimiter=',')
                    for row in reader:
                        if row[0]==lookFor:
                            print(row)
                            resultDict["type"].append((row[0], row[-5], row[-4], row[-3], row[-2], row[-1]))
            if len(resultDict["type"]) > 0:
                resultDict["sqliv"] = True
            else:
                resultDict["sqliv"] = False      
        except Exception as e:
            print(e)
        print(resultDict["type"])
    return resultDict

def __saveAnalysisResults(analysisResults, repoID, searchID):
    """Save the analysis result to database"""
    DB = Database()
    DB.connect()
    print(analysisResults['sqliv'])
    if analysisResults['sqliv'] is not None:
        sqliv = 1 if analysisResults["sqliv"] else 0
        DB.execute('''INSERT INTO result(search, repository, sqliv) VALUES(?,?,?)''',(searchID, repoID, sqliv))
    else:
        DB.execute('''INSERT INTO result(search, repository) VALUES(?,?)''',(searchID, repoID))
    lastRow = DB.lastRowID()
    print(analysisResults["type"])
    if len(analysisResults["type"]) > 0:
        for hit in analysisResults["type"]:
            file = hit[0]
            location = f'{hit[1]},{hit[2]},{hit[3]},{hit[4]}'
            DB.execute('''INSERT INTO sqliv_type(result, file_relative_repo, location) VALUES (?,?,?)''', (lastRow, file, location))
    DB.close()

if __name__ == '__main__':
    pass