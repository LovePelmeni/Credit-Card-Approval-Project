FROM python:3.9-slim-bullseye
LABEL maintainer=kirklimushin@gmail.com 

# Initializing Working Directory 
WORKDIR /project/dir/

# Defining Arguments
ARG HOME_DIR=/project/dir/
ARG UID=1000
ARG GID=1000

ARG user=python_user 
ARG group=python_group

# creating custom group
RUN groupadd -g "${GID}" python_group

# creating custom user and adding it to the group
RUN useradd --create-home -u "${UID}" -g "${GID}" python_user

# assigning access to the main directory
RUN chown python_user:python_group -R "${HOME_DIR}"

USER python_user

# Copying main content files to the Docker Image

COPY --chown="${user}":"${group}" ./src ./src
COPY --chown="${user}":"${group}" ./__init__.py ./
COPY --chown="${user}":"${group}" ./tests ./tests
COPY --chown="${user}":"${group}" ./module_requirements.txt ./
COPY --chown="${user}":"${group}" ./module_constraints.txt ./
COPY --chown="${user}":"${group}" ./entrypoint.sh ./
COPY --chown="${user}":"${group}" ./rest_controllers.py ./
COPY --chown="${user}":"${group}" ./settings.py ./

# Installing gcc compiler inside the image and updating repositories
RUN apt-get update -y && apt-get install -y gcc

# Installing basic dependencies

# RUN apt-get update \ 
# && apt-get install -y --no-install-recommends build-essential curl libq-dev \
# && apt-get clean

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