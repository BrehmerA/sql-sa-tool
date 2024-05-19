# README

## Introduction
This software is created for the purpose of analyzing open-source project on GitHub for SQL injection vulnerabilities over a large amount of open-source project and compile results for the analysis. This tool is utilizing other open source tools to perform some of the tasks included so be sure to read the requirements section before using the software. To run the tool clone or download the repository check that the requirements are met and run the main.py script.

### search parameters
The tool use github projects metrics as search parameters. In current version all parameters except language is set in the source code which is set in the CLI of the tool.
The parameters that can be set is:
*  Min and max number of stars. 
*  Min and max project size. 
*  Min number of contributors. 
These parameters can be set in the source code in main.py in line 12-17

### computer variable
In the CLI the computer choice is a simple mechanism to split a large search into three smaller peases.
Computer 1 handles middle range of stars. 36-500 for Java and 66-500 for python
Computer 2 handles high range of stars. 501 higher.
Computer 3 handles low range of stars. Up to 35 for Java and up to 65 for Python

Computer 1 and 2 do one search for each stars up to a number where there is less then 1000 projects with higher stars for which it makes one search.
Computer 3 handles low number of stars. For these searches the search also has to be split by size since there is more then 1000 results per star. In main.py on row 21 and 27 two dicts is defined which tells the program how to set the interval for the searches in computer 3. They work by defining how large range in size that should be included based on size and stars. E.i for search java for stars 0-5 and a size up to 300kb the step size is 0 which means that one search is performed for each size, if min size is 100 search are performed for 100,101,102... for each star. from 301-410kb projects the step size increase to 5kb so the first search here will be min_size = 301 and max_size = 306. This is done to keep the results below 1000 hits which is the maximum amount of results that can be extracted with GitHub search API. Notice that the levels was manually set according to the state of java and python projects at the time of writing the tool (spring 2024) and these should be revised before use since the base of project on GitHub is constantly evolving. 

## Requirements
To be able to use the tool you need to set up your environment accordingly. The following is needed to be set up for the tool to work.

Installation of git with git as system path.

*  Application is tested with Git version 2.39.0 and 2.44.0 but should work with versions supporting shallow cloning with the "git clone --depth x" command.

Application using curl for calls to the GitHub API.

</br>

A GitHub personal access token is required since the tool makes authenticated calls to the GitHub API. <span style="color:orange">Warning! Treat your access tokens like passwords.</span>

*  To create a personal access token follow instructions on github [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

*  Create a file called .token in the main folder and paste your GitHub Personal Access Token there. This file will be ignored by Git for security reasons.

</br>

The database that store the data is placed in main/database/database.db. The main branch contains an initialized empty database that are ready to use. In case a new database needs to be created. Create a new file main/database/database.db and run the sql command in main/database/sql/create.sql followed by main/database/sql/insert.sql to start on a new db.

