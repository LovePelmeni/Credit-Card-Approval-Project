from ...src.database import db_settings
from sqlalchemy import Engine

def test_database_connection():
    conn = db_settings.create_sql_engine()
    assert isinstance(conn, Engine)