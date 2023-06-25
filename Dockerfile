FROM --platform=arm64 python:3.9-buster 
LABEL maintainer=kirklimushin@gmail.com 

ARG ENV_NAME 
WORKDIR /project/dir/ 

RUN python3 -m venv ${ENV_NAME}
RUN source ./${ENV_NAME}/bin/activate 

RUN pip install --upgrade pip 
