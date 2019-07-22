# Iris Shim
Iris Shim parses abuse reports from the Iris data store. It currently supports parsing Phishing, Malware, Network Abuse and CSAM.

It performs a view core functions:
1. Parse emails from Iris
2. Validate the report excluding items (subjects, reporters, etc.) determined to be blacklisted
3. Provide feedback to reporters based on if we were able to successfully parse their report
4. Notate and close Iris incidents
5. Provide feedback to reporters based on if investigation is considered closed/resolved
6. Submit valid and reportable sources to the Abuse API for processing.

All of this functionality allows us to easily parse and submit tickets to the Abuse API that have been submitted via email.

## Cloning
 To clone the repository via SSH perform the following
 ```
 git clone git@github.secureserver.net:digital-crimes/iris_shim.git
 ```

 It is recommended that you clone this project into a pyvirtualenv or equivalent virtual environment.

## Installing Dependencies
To install all dependencies for development and testing simply run `make`.

 ## Deploying
This code can be deployed as a CRON job in any environment or simply run once. For running via CRON, first define your CRON file and initialize it (CentOs7 example) via
```
systemctl start crond
```
If you would like to run this script once then simply run `python run.py`

Note: You will still need to define all necessary environment variables. This can be done in the CRON file or elsewhere in your environment.

## Testing
```
make test     # runs all unit tests
make testcov  # runs tests with coverage
```

## Style and Standards

All deploys must pass Flake8 linting and all unit tests which are baked into the Makefile.

There are a few commands that might be useful to ensure consistent Python style:
```
make flake8  # Runs the Flake8 linter
make isort   # Sorts all imports
make tools   # Runs both Flake8 and isort
```

 ## Running Locally
 If you would like to run Iris Shim locally you will need to specify the following environment variables
1. `sysenv` (dev, ote, prod)
2. `IRIS_USERNAME` (User for IRIS)
3. `IRIS_PASSWORD` (Password for IRIS)
4. `API_KEY` (SSO Key for Abuse API)
5. `API_SECRET` (SSO Secret for Abuse API)
6. `OCM_CERT` (OCM CERT)
7. `OCM_KEY` (OCM KEY)
8. `EMAIL_RECIPIENT` (The email address you want non-shopper emails sent to while testing, instead of emailing the reporter. e.g. user@example.com)


The project can then be run locally by running `python run.py`
