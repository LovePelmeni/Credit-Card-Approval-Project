FROM python:3.10-bullseye
LABEL maintainer=kirklimushin@gmail.com 

# root user's username
ARG ROOT_USER=python_user

# Environment Project Variables
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONUNBUFFERED=0

# creating root user and assigning sudo privileges

RUN useradd -ms /bin/bash ${ROOT_USER}
RUN usermod -aG sudo ${ROOT_USER}

# Initializing Working Directory 
WORKDIR /project/dir/${ROOT_USER}

# Copying main content files to the Docker Image

COPY  ./src ./src
COPY  ./__init__.py ./
COPY  ./tests ./tests
COPY  ./proj_requirements ./proj_requirements
COPY  ./env ./env
COPY  ./deployment/entrypoint.sh ./
COPY  ./deployment/database.sh ./
COPY  ./rest_controllers.py ./
COPY  ./py_logging.py ./
COPY  ./settings.py ./
COPY  ./exc_handlers.py ./

# Copying additional configuration files
COPY ./tox.ini ./
COPY ./pyproject.toml ./
COPY ./poetry.lock ./

# Creating directory for storing log files 
RUN mkdir logs

# Installing gcc compiler inside the image and updating repositories
RUN apt-get update -y && apt-get install -y gcc

# upgrading pip packet manager 
RUN pip install --upgrade pip

# Installing poetry manager for Python
RUN pip install poetry --upgrade

# Updating Production Requirements for the Project using Poetry

RUN poetry install --no-dev 

# Export production requirements using Poetry
RUN poetry export --format=requirements.txt --output proj_requirements/prod_requirements.txt --without-hashes

# Install production dependencies with pip
RUN pip install -r ./proj_requirements/prod_requirements.txt

# upgrading fastapi web framework packages  
RUN pip install 'fastapi[all]' --upgrade

# Giving acccess to the shell script
RUN chmod +x ./entrypoint.sh
RUN chmod +x ./database.sh

# Running entrypoint deployment script
ENTRYPOINT ./entrypoint.sh