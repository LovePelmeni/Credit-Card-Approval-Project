#!/bin/bash 

alembic revision --autogenerate -m "Initial Migrations"

if [ $? -ne 0 ]; then 
    echo "Failed to build initial migrations"
else    
    echo "Migrations has been initialized"
fi

alembic upgrade head 


if [ $? -ne 0 ]; then 
    echo "Failed to apply migrations to the database, are you sure it's running?"
else
    echo "Migrations has been applied successfully"
fi