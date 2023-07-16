FROM python:3.9-slim-bullseye
LABEL maintainer=kirklimushin@gmail.com 

# root user's username
ENV ROOT_USER=python_user
ENV APPLICATION_PORT=8080

# creating root user and assigning sudo privileges

RUN useradd -ms /bin/bash ${ROOT_USER}
RUN usermod -aG sudo ${ROOT_USER}

# Initializing Working Directory 
WORKDIR /project/dir/${ROOT_USER}

# Copying main content files to the Docker Image

COPY  ./src ./src
COPY  ./__init__.py ./
COPY  ./tests ./tests
COPY  ./module_requirements.txt ./
COPY  ./module_constraints.txt ./
COPY  ./entrypoint.sh ./
COPY  ./rest_controllers.py ./
COPY  ./settings.py ./

# Installing gcc compiler inside the image and updating repositories
RUN apt-get update -y && apt-get install -y gcc

# upgrading pip packet manager 
RUN pip install --upgrade pip 
RUN pip install --upgrade setuptools wheel

# installing dependencies inside virtual environment
RUN pip install -r module_requirements.txt -c module_constraints.txt

# upgrading fastapi web framework packages  
RUN pip install 'fastapi[all]' --upgrade

HEALTHCHECK --interval=30s --timeout=5s \
CMD curl -f "http://localhost:${APPLICATION_HOST}/healthcheck/" || (echo "Server did not respond!" && exit 1); 

# Giving acccess to the shell script
RUN chmod +x ./entrypoint.sh

# Running entrypoint deployment script
ENTRYPOINT ./entrypoint.sh