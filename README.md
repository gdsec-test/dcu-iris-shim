# Iris Shim

## Overview
Iris Shim parses abuse reports from the Iris data store. It currently supports parsing Phishing, Malware, Network Abuse and CSAM.

It performs a view core functions:
1. Parse emails from Iris
2. Validate the report excluding items (subjects, reporters, etc.) determined to be blacklisted
3. Provide feedback to reporters based on if we were able to successfully parse their report
4. Notate and close Iris incidents
5. Provide feedback to reporters based on if investigation is considered closed/resolved
6. Submit valid and reportable sources to the Abuse API for processing.

All of this functionality allows us to easily parse and submit tickets to the Abuse API that have been submitted via email.

## Table of Contents
  1. [Cloning](#cloning)
  2. [Installing Dependencies](#installing-dependencies)
      1. [Ubuntu Based System Dependencies](#ubuntu-based-system-dependencies)
      2. [Project Dependencies](#project-dependencies)
  3. [Building](#building)
  4. [Deploying](#deploying)
  5. [Testing](#testing)
  6. [Style and Standards](#style-and-standards)
  7. [Running Locally](#running-locally)

## Cloning
 To clone the repository via SSH perform the following

 ```
 git clone git@github.secureserver.net:digital-crimes/iris_shim.git
 ```

 It is recommended that you clone this project into a pyvirtualenv or equivalent virtual environment.

## Installing Dependencies
### Ubuntu Based System Dependencies
For connecting to the IRIS DB locally with a Ubuntu based development system, you will need to ensure that you have the ODBC Driver Manager packages installed and FreeTDS driver settings specified.
```
sudo apt-get install unixodbc-dev unixodbc-bin unixodbc
```

Edit your odbcinst.ini file. 
```
sudo vim /etc/odbcinst.ini
```
Add the following info for the FreeTDS Driver and save the file.
```
[FreeTDS]
Description = TDS driver (Sybase/MS SQL)
# Some installations may differ in the paths
Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so
Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so
CPTimeout =
CPReuse =
FileUsage = 1
TDS Version = 8.0
```

### Project Dependencies
To install all dependencies for development and testing simply run `make`.

## Building
Building a local Docker image for the respective development environments can be achieved by

```
make [dev, prod]
```

## Deploying
Deploying the Docker image to Kubernetes can be achieved via

```
make [dev, prod]-deploy
```

You must also ensure you have the proper push permissions to Artifactory or you may experience a `Forbidden` message.

## Testing
```
make test     # runs all unit tests
make testcov  # runs tests with coverage
```

## Style and Standards

All deploys must pass Flake8 linting and all unit tests which are baked into the [Makefile](Makefile).

There are a few commands that might be useful to ensure consistent Python style:
```
make flake8  # Runs the Flake8 linter
make isort   # Sorts all imports
make tools   # Runs both Flake8 and isort
```

 ## Running Locally
 If you would like to run Iris Shim locally you will need to specify the following environment variables
* `sysenv` (dev, prod)
* `IRIS_USERNAME` (User for IRIS)
* `IRIS_PASSWORD` (Password for IRIS)
* `API_KEY` (SSO Key for Abuse API)
* `API_SECRET` (SSO Secret for Abuse API)
* `OCM_CERT` Path to phishstory.int certificate file (for sending mail via Hermes)
* `OCM_KEY` Path to phishstory.int key file (for sending mail via Hermes)
* `EMAIL_RECIPIENT` (The email address you want non-shopper emails sent to while testing, instead of emailing the reporter. e.g. user@example.com)


The project can then be run locally by running `python run.py`
