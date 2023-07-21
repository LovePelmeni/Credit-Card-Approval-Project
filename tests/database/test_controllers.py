import unittest.mock
from src.database import db_controllers
import pandas, typing 

def transaction_dataset() -> pandas.DataFrame:
    """
    Function returns mocked transaction dataset for testing 
    CREATE DB Controller
    """

def mocked_stratified_dataset() -> typing.Dict[str, typing.List]:
    """
    Function returns mocked data for training ML Models 
    using Database user Session
    """

trans_dataset = transaction_dataset()
strat_dataset = mocked_stratified_dataset()

@unittest.mock.patch(target='src.database.db_controllers.user_session.execute')
def test_create_new_transaction(mocked_session):
    mocked_session.return_value = True 
    created = db_controllers.create_transaction()
    assert created == True

@unittest.mock.patch(target="src.database.db_controllers.user_session.execute")
def test_databaset_loader(mocked_session):
    mocked_session.returns_value = strat_dataset
    data = db_controllers.get_records_dataset(samples_per_category=5)
    assert isinstance(data, pandas.DataFrame)
