import pytest
from src.main.api.db.engine import SessionLocal, engine
import src.main.api.db.models.user_table
import src.main.api.db.models.account_table
import src.main.api.db.models.credit_table
import src.main.api.db.models.transaction_table

@pytest.fixture(scope="session")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()