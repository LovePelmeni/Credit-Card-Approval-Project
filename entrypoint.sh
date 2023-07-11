#!/bin/bash

echo "Starting Entrypoint pipeline...."

echo "Activating Virtual Environment"

pip list

ls

echo "Running Unittests..."

pytest ./unittests

if [ $? -ne 0 ]; then
    echo "Unittests Failed"
    exit 1
else
    echo "Unittests have run successfully"
fi

echo "Starting ASGI Server..."

python ./settings.py

if [ $? -ne 0 ]; then
    echo "ASGI Server Startup Failure"
    exit 1
fi
