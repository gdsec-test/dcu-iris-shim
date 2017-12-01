# Iris Shim
Iris Shim pulls tickets from the phishing, malware, and network abuse queues in Iris, closes the tickets, and submits them to the Abuse API.

This allows us to easily parse and submit tickets to the Abuse API automation that have been submitted via email.

## Cloning
 To clone the repository via SSH perform the following
 ```
 git clone git@github.secureserver.net:ITSecurity/iris_shim.git
 ```

 It is recommended that you clone this project into a pyvirtualenv or equivalent virtual environment.

## Installing Dependencies
You can install the required dependencies via
```
pip install -r requirements.txt
```

 ## Deploying
This code can be deployed as a CRON job in any environment or simply run once. For running via CRON, first define your CRON file and initialize it (CentOs7 example) via
```
systemctl start crond
```
If you would like to run this script once then simply run `python run.py`

Note: You will still need to define all necessary environment variables. This can be done in the CRON file or elsewhere in your environment.
 

 ## Testing
 In order to run the tests you must first install the required dependencies via
 ```
 pip install -r test_requirements.txt
 ```

 After this you may run the tests via
 ```
 nosetests tests/
 ```

 Optionally, you may provide the flags `--with-coverage --cover-package=./` to `nosetests` to determine the test coverage of the project.


 ## Running Locally
 If you would like to run Iris Shim locally you will need to specify the following environment variables
 1. `sysenv` (dev, ote, prod)
 2. `key` 
 3. `secret` 
 4. `SMDB_USER` 
 5. `SMDB_PASS`

The project can then be run locally by running `python run.py`