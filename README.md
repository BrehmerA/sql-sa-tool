# README

## Requirements
To be able to use the tool you need to set up your environment accordingly. The following is needed to be set up for the tool to work.

Installation of git with git as system path.  
* Application is tested with Git version 2.39.0 to 2.44.0 but should work with versions supporting shallow cloning with the "git clone --depth x" command.

</br>

Installation of codeQL CLI with the requirement of setting codeQL as system path.  
* Installation instructions [here](https://docs.github.com/en/code-security/codeql-cli/getting-started-with-the-codeql-cli/setting-up-the-codeql-cli)  

* The application is currently only tested with codeQL CLI version 2.16.3.

</br>

A GitHub personal access token is required since the tool makes authenticated calls to the GitHub API. <span style="color:orange">Warning! Treat your access tokens like passwords.</span>  
* To create a personal access token follow instructions on github [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)  
* Create a file called .token in the main folder and paste your GitHub Personal Access Token there. This file will be ignored by Git for security reasons.
