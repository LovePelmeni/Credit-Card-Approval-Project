FROM --platform=arm64 python:3.9-buster 
LABEL maintainer=kirklimushin@gmail.com 

ARG ENV_NAME 

WORKDIR /project/dir/ 

RUN python3 -m venv ${ENV_NAME}
RUN source ./${ENV_NAME}/bin/activate 

RUN pip install --upgrade pip 

# Copying Project dependencies inside the directory 

COPY ./src ./
COPY ./unittests ./
COPY ./entrypoint.sh ./
COPY ./module_requirements.txt ./
COPY ./module_constraints ./

# Allowing Access for running shell deployment script 
RUN chmod +x ./entrypoint.sh 
ENTRYPOINT ["sh", "./entrypoint.sh"]
