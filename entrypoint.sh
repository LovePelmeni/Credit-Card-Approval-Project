#!/bin/bash

echo "Starting Entrypoint pipeline...."

echo "Activating Virtual Environment"

pip list

ls

echo "Running Unittests..."

pytest tests

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
