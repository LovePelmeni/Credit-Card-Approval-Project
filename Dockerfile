FROM python:3.9-slim-buster
LABEL maintainer=kirklimushin@gmail.com 

WORKDIR /project/dir/

# Copying main content files to the Docker Image

COPY ./src ./
COPY ./__init__.py ./
COPY ./unittests ./
COPY ./module_requirements.txt ./
COPY ./module_constraints.txt ./
COPY ./entrypoint.sh ./
COPY ./rest_controllers.py ./
COPY ./settings.py ./

# upgrading pip packet manager 
RUN pip install --upgrade pip 
RUN pip install --upgrade setuptools wheel

# installing dependencies inside virtual environment
RUN pip install -r module_requirements.txt -c module_constraints.txt

# Giving acccess to the shell script
RUN chmod +x ./entrypoint.sh

# Running entrypoint deployment script
ENTRYPOINT ./entrypoint.sh