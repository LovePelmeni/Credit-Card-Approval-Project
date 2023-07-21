#!/bin/bash

echo "Starting Entrypoint pipeline...."

echo "Activating Virtual Environment"

pip list

echo "Available PIP modules"
ls 

echo "Updating code style using autopep8"

autopep8 . --recursive --in-place 

echo "Checking Code Style using flake8..."

flake8 .

if [ $? -ne 0 ]; then 
    echo "Codestyle Failed tests..."
    exit 1
else
    echo "Codestyle is fine..."
fi

echo "Running Unittests..."

python -m pytest

if [ $? -ne 0 ]; then
    echo "Unittests Failed"
    exit 1
else
    echo "Unittests have run successfully"
fi

echo "Starting ASGI Server..."

uvicorn settings:application --host 0.0.0.0 --port 8080

if [ $? -ne 0 ]; then
    echo "ASGI Server Startup Failure"
    exit 1
fi
