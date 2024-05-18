# README

## Introduction
This software is created for the purpose of analyzing open-source project on GitHub for SQL injection vulnerabilities over a large amount of open-source project and compile results for the analysis. This tool is utilizing other open source tools to perform some of the tasks included so be sure to read the requirements section before using the software. To run the tool clone or download the repository check that the requirements are met and run the main.py script.

### search parameters
The tool let the user define parameters to use during the search. The parameters are presented below with defaults and possible values.

*  Language: Java or Pyhton with Java as default.

*  min size: positive int, default 100b

*  max size: positive int, default no max value

*  min number of stars: positive int, default 2

*  max number of stars: positive int, default no max value

*  min number of contributors: positive int, default 2

*  max number of contributors: positive int, default no max value

## Requirements
To be able to use the tool you need to set up your environment accordingly. The following is needed to be set up for the tool to work.

Installation of git with git as system path.

*  Application is tested with Git version 2.39.0 and 2.44.0 but should work with versions supporting shallow cloning with the "git clone --depth x" command.

Application using curl for calls to the GitHub API.

</br>

A GitHub personal access token is required since the tool makes authenticated calls to the GitHub API. <span style="color:orange">Warning! Treat your access tokens like passwords.</span>

*  To create a personal access token follow instructions on github [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

*  Create a file called .token in the main folder and paste your GitHub Personal Access Token there. This file will be ignored by Git for security reasons.

