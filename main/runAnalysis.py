import csv
import ntpath
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path

from database.database import Database

DBDriverJavaObjectFunction = ['Statement', 'ResultSet', 'PreparedStatement', 'TypedQuery'] # TODO Extend.
DBDriverPythonImports = ['pymssql', 'asyncpg', 'pyodbc', 'sqlite3', 'mysql.connector', 'psycopg', 'psycopg2', 'pymysql', 'mysqlclient']
codeQLDB = 'codeQLDBmap'
SQL_KEY_WORDS = [r'SELECT', r'UPDATE', r'INSERT', r'DELETE', r'CREATE', r'ALTER', r'DROP']
keyWordString = r'('+r'|'.join(SQL_KEY_WORDS)+r')'
concatPlusSign = r'((\"|\').*'+keyWordString+r'\b.*(\"|\')\s*\+\s*\w+)+'
concatAppendJ = r'(append\s*\(\s*"'+keyWordString+r'\b.*"\s*\)\s*\.\s*append\s*\(\s*\w*\s*\))+'
concatFormatJ = r'(String\s*\.\s*format\s*\(\s*"\s*'+keyWordString+r'\b.*%s.*"\s*,\s*\w+\s*\))+'
concatFormatP = r'(.*"\s*'+keyWordString+r'\b.*"\s*\.\s*format\s*\((\s*\w+\s*)(,\s*\w+\s*)*\))+'
concatPercentP = r'((\'|\")\s*'+keyWordString+r'\b.*?(%s|%d).*?(\'|\")\s*%\s*\()+'

def search(lang, path, repo, repoID, searchID):
    baseName = ntpath.basename(repo)[:-4]
    cloneInto = Path(path + '/' + baseName)
    complete = subprocess.run(
        ['git', 'clone', '--depth', '1', repo , cloneInto],
        stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT,
    )
    if __searchFiles(complete, lang):
        analysisResults = __performSQLIVAnalysis(cloneInto, lang)
        __saveAnalysisResults(analysisResults, repoID, searchID)
    else:
        print(f'No SQL connection found in {str(cloneInto)}.')
    try:
        for root, dirs, files in os.walk(cloneInto):
            for dir in dirs:
                os.chmod(os.path.join(root, dir), stat.S_IRWXU)
            for file in files:
                os.chmod(os.path.join(root, file), stat.S_IRWXU)
        shutil.rmtree(cloneInto)
    except Exception as e:
        print(f'Problem deleting file in {str(cloneInto)}.')
        print(e)


def __searchFiles(complete, lang) -> bool:
        """Search cloned repos for db drivers. Search all files in repo with lang extension stop search for repo at first find."""

        dirPath = complete.args[5]
        extension = ''
        searchRegex = ''
        found = False
        if lang == 'Python':
            extension = '*.py'
            searchRegex = __createSearchRegexPython()
        elif lang == 'Java':
            extension = '*.java'
            searchRegex = __createSearchRegexJava()
        for file in list(dirPath.rglob(extension)):
            try:
                f=open(file)
            except FileNotFoundError:
                print('File not found.')
            except PermissionError:
                print('No permission to open file.')
            except:
                print('Unknown error.')
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
    """Define the search regex for the Java DB drivers."""

    classNames = ''
    for c in DBDriverJavaObjectFunction:
        classNames = classNames + c + '|'
    regex = r'^(?=.*\b('+classNames+r')\b).*$'
    return regex


def __createSearchRegexPython() -> str:
    """Define the search regex for the Python DB drivers."""

    drivers = ''
    for driver in DBDriverPythonImports:
        drivers = drivers + driver + '|'
    drivers = drivers[:-1]
    regex = r'^(?=.*\b(import)\b)(?=.*\b('+drivers+r')\b).*$'
    return regex


def __performSQLIVAnalysis(cloneInto: Path, lang: str) -> dict:
    """Perform the codeQL analysis and save results to the DB."""

    regexSet = []
    extension = ''
    if lang == 'Python':
        regexSet.append(concatPlusSign, concatFormatP, concatPercentP)
        extension = '*.py'
    elif lang == 'Java':
        regexSet.append(concatPlusSign, concatAppendJ, concatFormatJ)
        extension = '*.java'
    print(regexSet)
    resultDict = {
        'sqliv' : None,
        'type' : [],
    }
    for file in list(cloneInto.rglob(extension)):
            try:
                f=open(file)
            except FileNotFoundError:
                print('File not found.')
            except PermissionError:
                print('No permission to open file.')
            except:
                print('Unknown error.')
            else:
                with f as fp:
                    text = fp.read()
                    for reg in regexSet:
                        for match in re.finditer(reg, text, re.IGNORECASE):
                            resultDict['type'].append(__index_to_coordinates(fp, text, match.start(), match.end()))
    return resultDict

def __index_to_coordinates(file, s : str, indexStart : int, indexEnd : int) -> list:
    """Returns (filename, line_number, col_start, line:number, col_end) of `index` in `s`."""
    
    if not len(s):
        return 1, 1
    sp = s[:indexEnd+1].splitlines(keepends=True)
    line = len(sp)
    end = len(sp[-1])
    start = end - (indexEnd-indexStart)
    return [file.name, line, start, line,  end]

def __saveAnalysisResults(analysisResults, repoID, searchID):
    """Save the analysis result to database."""

    DB = Database()
    DB.connect()
    repoQuery = DB.fetch_one('''SELECT number_of_stars, size, number_of_followers, number_of_contributors from repository WHERE id=?''', (repoID,))
    if analysisResults['sqliv'] is not None:
        sqliv = 1 if analysisResults['sqliv'] else 0
        DB.execute('''INSERT INTO result(search, repository, sqliv, number_of_stars, size, number_of_followers, number_of_contributors) VALUES (?, ?, ?, ?, ?, ?, ?)''', (searchID, repoID, sqliv, repoQuery[0], repoQuery[1], repoQuery[2], repoQuery[3]))
    else:
        DB.execute('''INSERT INTO result(search, repository, number_of_stars, size, number_of_followers, number_of_contributors) VALUES (?, ?, ?, ?, ?, ?)''', (searchID, repoID, repoQuery[0], repoQuery[1], repoQuery[2], repoQuery[3]))
    lastRow = DB.last_row_id()
    print(analysisResults['type'])
    if len(analysisResults['type']) > 0:
        for hit in analysisResults['type']:
            file = hit[0]
            location = f'{hit[1]},{hit[2]},{hit[3]},{hit[4]}'
            DB.execute('''INSERT INTO sqliv_type(result, file_relative_repo, location) VALUES (?,?,?)''', (lastRow, file, location))
    DB.close()


if __name__ == '__main__':
    pass
