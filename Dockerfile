FROM python:3.9-slim
LABEL maintainer=kirklimushin@gmail.com 

WORKDIR /project/dir/

# Copying main content files to the Docker Image

COPY ./src ./src
COPY ./__init__.py ./
COPY ./tests ./tests
COPY ./module_requirements.txt ./
COPY ./module_constraints.txt ./
COPY ./entrypoint.sh ./
COPY ./rest_controllers.py ./
COPY ./settings.py ./

# Installing gcc compiler inside the image and updating repositories
RUN apt-get update -y && apt-get install -y gcc

# upgrading pip packet manager 
RUN pip install --upgrade pip 
RUN pip install --upgrade setuptools wheel

# installing dependencies inside virtual environment
RUN pip install -r module_requirements.txt -c module_constraints.txt

# Giving acccess to the shell script
RUN chmod +x ./entrypoint.sh

# Running entrypoint deployment script
ENTRYPOINT ./entrypoint.sh