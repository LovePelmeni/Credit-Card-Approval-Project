FROM python:3.9-slim-bullseye
LABEL maintainer=kirklimushin@gmail.com 

# root user's username
ARG ROOT_USER=python_user

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
COPY  ./deployment/entrypoint.sh ./
COPY  ./rest_controllers.py ./
COPY  ./settings.py ./
COPY ./tox.ini ./
COPY ./pyproject.toml ./
COPY ./poetry.lock ./


# Installing gcc compiler inside the image and updating repositories
RUN apt-get update -y && apt-get install -y gcc

# upgrading pip packet manager 
RUN pip install --upgrade pip

# Installing poetry manager for Python
RUN pip install poetry --upgrade

# Updating Production Requirements for the Project using Poetry
RUN poetry export --format=requirements.txt --output proj_requirements/prod_requirements.txt

# installing dependencies inside virtual environment
RUN pip install -r ./proj_requirements/proj_requirements.txt \ 
-c ./proj_requirements/module_constraints.txt

# upgrading fastapi web framework packages  
RUN pip install 'fastapi[all]' --upgrade

# Giving acccess to the shell script
RUN chmod +x ./entrypoint.sh

# Running entrypoint deployment script
ENTRYPOINT ./entrypoint.sh