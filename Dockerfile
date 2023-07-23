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

# Installing gcc compiler inside the image and updating repositories
RUN apt-get update -y && apt-get install -y gcc

# upgrading pip packet manager 
RUN pip install --upgrade pip

# installing dependencies inside virtual environment
RUN pip install -r ./proj_requirements/module_requirements.txt \ 
-c ./proj_requirements/module_constraints.txt

# upgrading fastapi web framework packages  
RUN pip install 'fastapi[all]' --upgrade

# Giving acccess to the shell script
RUN chmod +x ./entrypoint.sh

# Running entrypoint deployment script
ENTRYPOINT ./entrypoint.sh