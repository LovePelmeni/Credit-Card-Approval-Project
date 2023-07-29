#!/bin/bash 

IMAGE_NAME="$1" # name of the image to recreate
BUILD_LOCATION="$2" # build location of the Dockerfile

docker rmi ${IMAGE_NAME} && docker build ${BUILD_LOCATION} -t ${IMAGE_NAME}

if [ $? -ne 0 ]; then
    echo "Failed to rebuild project's image"
    exit 1;
else 
    echo "Image has been recreated successfully."
    exit 0;
fi