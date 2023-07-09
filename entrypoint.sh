#!/bin/sh 

echo "Starting Entrypoint pipeline...."

echo "Activating Virtual Environment"

activate () {
    . ./fn_env/bin/activate
}

activate

echo "Running Unittests..."

pytest unittests

if [$? -ne 0 ]; then 
    echo "Unittests Failed"
    exit 1;
else 
    echo "Unittests has run successfully"
fi 

echo "Starting ASGI Server..."

python settings.py

if [$? -ne 0 ]; then 
    echo "ASGI Server Startup Failure"
    exit 1; 
fi 