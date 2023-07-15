FROM python:3.9-slim-bullseye
LABEL maintainer=kirklimushin@gmail.com 

# Initializing Working Directory 
WORKDIR /project/dir/

# Defining Arguments
ARG HOME_DIR=/project/dir/
ARG UID=1001
ARG GID=1001

ARG user=python_user 
ARG group=python_group

# Copying main content files to the Docker Image

COPY  ./src ./src
COPY  ./__init__.py ./
COPY  ./tests ./tests
COPY  ./module_requirements.txt ./
COPY  ./module_constraints.txt ./
COPY  ./entrypoint.sh ./
COPY  ./rest_controllers.py ./
COPY  ./settings.py ./

# creating custom group
RUN groupadd -g "${GID}" "${group}"

# creating custom user and adding it to the group
RUN useradd --create-home -u "${UID}" -g "${GID}" "${user}"

USER "${user}"

# assigning access to the main directory
RUN chown python_user:python_group -R "${HOME_DIR}"

# Installing gcc compiler inside the image and updating repositories
RUN apt-get update -y && apt-get install -y gcc

# upgrading pip packet manager 
RUN pip install --upgrade pip 
RUN pip install --upgrade setuptools wheel

# installing dependencies inside virtual environment
RUN pip install -r module_requirements.txt -c module_constraints.txt

# defining healthchecks strategy
HEALTHCHECK --interval=30s --timeout=5s \
cmd curl -f "http://${APPLICATION_HOST}:${APPLICATION_PORT}" || echo "server did not respond!" && exit 1

# Giving acccess to the shell script
RUN chmod +x ./entrypoint.sh

# Running entrypoint deployment script
ENTRYPOINT ./entrypoint.sh