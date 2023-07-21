#!/bin/bash

echo "Building Project..."

docker build . --env-file='environment.env'

echo "Great! Project is up and running. Access via `docker run --name <container-name> <image-id> -p 8000:8000"


