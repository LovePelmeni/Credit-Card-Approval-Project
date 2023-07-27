from sqlalchemy.engine import create_engine as create_sql_engine, Engine
from sqlalchemy.orm import sessionmaker
import psycopg2.errors
import logging

from pathlib import Path
import configparser
import os 

if os.environ.get("TESTING_MODE", 1) == 0:
    Logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler(filename="../../logs/db_settings.log")
    Logger.addHandler(file_handler)
else:
    Logger = logging.getLogger(__name__)
    
DATABASE_NAME = os.environ.get("POSTGRES_NAME", "postgres")
DATABASE_USER = os.environ.get("POSTGRES_USER", "postgres")
DATABASE_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgres")
DATABASE_HOST = os.environ.get("POSTGRES_HOST", "localhost")
DATABASE_PORT = os.environ.get("POSTGRES_PORT", "5434")

if not all(
    [
        DATABASE_NAME, DATABASE_USER, 
        DATABASE_PASSWORD, 
        DATABASE_HOST, DATABASE_PORT
    ]):
    raise SystemExit(
        "Some of Database Required Parameters are missing, make sure you have set up env variables"
    )

DATABASE_URL = "postgresql://%s:%s@%s:%s/%s" % (
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_NAME
)

def update_configuration_file():
    """
    Function updates internal alembic configuration file to dynamically set
    current database url, that sqlalchemy use
    """
    config = configparser.ConfigParser()
    full_path = os.path.join("src/database", "alembic.ini")
    print(full_path)
    alem_file = Path(full_path)  #Path of your .ini file
    config.read(alem_file)

    config.set('alembic', 'sqlalchemy.url', DATABASE_URL) #Updating existing entry 
    config.write(alem_file.open("w"))


def create_engine(database_url: str) -> Engine:
    """
    Function creates new database engine, based on provided
    `database_url`
    NOTE:   
        url should include:
            host, port, user, password and database_name
    Args:
        database_url: URL of the database to connect 
    Returns:
        Database Engine Object
    """
    try:
        update_configuration_file()
        new_engine = create_sql_engine(
            url=database_url
        )
        return new_engine
    except Exception as err:
        Logger.critical(err)
        raise SystemExit("Database Connection Failure")


def get_user_session() -> sessionmaker:
    """
    Function creates user default session 
    """
    try:
        user_session = sessionmaker(
            bind=new_engine,
            autoflush=False
        )
        return user_session()
    except(psycopg2.errors.ProgrammingError, 
    psycopg2.errors.CannotConnectNow) as conn_err:
        Logger.critical(conn_err)
        raise SystemExit("Failed to get user session")


new_engine = create_engine(DATABASE_URL) 

# Initializing basics ORM Table Abstraction 

from sqlalchemy.orm import declarative_base

Model = declarative_base()