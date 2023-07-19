from sqlalchemy.engine import create_engine as create_sql_engine, Engine
from sqlalchemy.orm import sessionmaker
import os
import psycopg2.errors
import logging

from pathlib import Path
import configparser

Logger = logging.getLogger(__name__)

DATABASE_NAME = os.environ.get("DATABASE_NAME", "postgres")
DATABASE_USER = os.environ.get("DATABASE_USER", "postgres")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "postgres")
DATABASE_HOST = os.environ.get("DATABASE_HOST", "localhost")
DATABASE_PORT = os.environ.get("DATABASE_PORT", "5434")

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
    alem_file = Path('alembic.ini')  #Path of your .ini file
    config.read(alem_file)

    config.set('alembic', 'sqlalchemy.url', DATABASE_URL) #Updating existing entry 
    config.write(alem_file.open("w"))

update_configuration_file()



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
        new_engine = create_sql_engine(
            url=database_url
        )
        return new_engine
    except(psycopg2.errors.ConnectionException) as err:
        Logger.critical(err)
        raise RuntimeError("Database Connection Failure")

new_engine = create_engine(DATABASE_URL) 

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
        raise RuntimeError("Failed to get user session")

class DatabaseSession(object):
    """
    Standard Interface for database session
    """
    def __init__(self, session):
        self.session = session 

    def __enter__(self):
        return self.session

    def __exit__(self):
        self.session.close()

# Initializing basics ORM Table Abstraction 

from sqlalchemy.orm import declarative_base

Model = declarative_base()