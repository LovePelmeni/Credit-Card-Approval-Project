FROM --platform=arm64 python:3.9-buster 
LABEL maintainer=kirklimushin@gmail.com 

ARG ENV_NAME 

WORKDIR /project/dir/ 

RUN python3 -m venv ${ENV_NAME}
RUN source ./${ENV_NAME}/bin/activate 

RUN pip install --upgrade pip 

COPY ./src ./
COPY ./unittests ./
COPY ./module_requirements.txt ./
COPY ./entrypoint.sh ./

RUN pip freeze > module_requirements.txt
RUN pip install -r module_requirements.txt -c ./module_constraints.txt
RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["sh", "./entrypoint.sh"]