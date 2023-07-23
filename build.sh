#!/bin/bash 

echo "Updating project module requirements versions..."

cd proj_requirements/
sh 'poetry export --output=requirements.txt --output=module_requirements.txt --without-hashes'
cd ..

echo "Building Project...."
docker-compose up -d

if [ $? -ne 0 ]; then 
    echo "Failed to build Project, exiting..."
    exit 1;
else 
    echo "Project was built successfully!"
fi