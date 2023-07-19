import sqlalchemy
from sqlalchemy.engine import Engine 
from sqlalchemy.orm import sessionmaker
import os
import psycopg2.errors
import logging, typing

Logger = logging.getLogger(__name__)

DATABASE_NAME = os.environ.get("DATABASE_NAME", None)
DATABASE_USER = os.environ.get("DATABASE_USER", None)
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", None)
DATABASE_HOST = os.environ.get("DATABASE_HOST", None)
DATABASE_PORT = os.environ.get("DATABASE_PORT", None)

DATABASE_URL = "psql://%s:%s@%s:%s/%s" % (
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_USER,
    DATABASE_PASSWORD,
    DATABASE_NAME
)

def create_engine(database_url: str) -> typing.Generator[Engine]:
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
        new_engine = Engine(
            url=database_url, 
            pool=True
        )
        yield new_engine
    except(psycopg2.errors.ConnectionException) as err:
        Logger.critical(err)
        raise RuntimeError("Database Connection Failure")

new_engine = create_engine(DATABASE_URL) 

def get_user_session() -> typing.Generator[sessionmaker]:
    """
    Function creates user default session 
    """
    try:
        user_session = sessionmaker(
            bind=new_engine,
            autoflush=False
        )
        yield user_session()
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