<div style="text-align:center; margin-bottom: 30px">
  <h2> Credit Card Approval Project</h2>
</div>

[comment]: <> ("Docs Badges goes there")

<div class="container badges" 
style="display: flex; justify-content: center; column-gap: 5px; margin-bottom: 30px">

<a href="https://github.com/badges/shields/pulse" alt="Activity">
        <img src="https://img.shields.io/badge/version-1.2.3-blue" /></a>

<a href="https://github.com/badges/shields/pulse" alt="Activity">
        <img src="https://img.shields.io/github/commit-activity/m/badges/shields" /></a>
    
<a href="https://circleci.com/gh/badges/shields/tree/master">
    <img src="https://img.shields.io/circleci/project/github/badges/shields/master" alt="build status">
</a>
    
<a href="https://circleci.com/gh/badges/daily-tests">
    <img src="https://img.shields.io/circleci/project/github/badges/daily-tests?label=service%20tests" alt="service-test status">
</a>

<a href="https://coveralls.io/github/badges/shields">
    <img src="https://img.shields.io/coveralls/github/badges/shields"
            alt="coverage">
</a>

</div>

<div style="margin-bottom: 40px">

This is home to `Credit Card Approval Project`, an offline machine learning model
for predicting credit card approval, based on your personal information, including client's credit intentions and fcredit window. Deployed it using modern `FastAPI` python web framework.

</div> 

## Technologies 

1. *Python* (main backend language, both for ML and Web deployment)
2. *Docker* and *Docker-Compose* (for containerization)
3. *Bash Scripting* (for creating deployment pipeline)
4. *PostgreSQL* (database for storing user's information about the project)

## Versioning

1. `3.9` <= Python <= `3.10`
2. Docker >= `20.10.12`
3. Docker-Compose >= `1.29.2`
3. GNU bash >= `3.2.57`


## Directory overview 

`src` - contains all source code for the project, including ML models and Datasets

`env` - Environment Variables for the project 

`deployment` - deployment files and bash scripts

`docs` - contains documentation for the project 

`tests` - contains tests 

`proj_requirements` - contains project dependencies instructions 


# Usage

### Clone project using following command

```
$ git clone https://github.com/LovePelmeni/Credit-Card-Approval-Project.git
```

## Local Development
### Setting up Python Virtual Environment

```
# Creating new virtual environment

$ python3 -m venv fn_env
$ source ./fn_env/bin/activate 
```
### Installing project dependencies

```
$ pip install -r proj_requirements/module_requirements.txt -c proj_requirements/module_constraints.txt
```

### Run shell script called `local_dev.sh`
```
$ chmod +x ./local_dev.sh
$ sh ./local_dev.sh
```

## Deployment

### Running project using Docker-Compose

```
$ docker-compose up -d
```
In case you don't want to keep cache of this image add `--no--cache` flag

## Testing Application 
