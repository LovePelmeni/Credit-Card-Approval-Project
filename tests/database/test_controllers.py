import unittest.mock
from ...src.database import db_manager
import pandas
import pytest 
import typing
import pytest


@pytest.fixture(scope="module")
def dataset() -> typing.List:
    """
    Function returns mocked raw dataset, parsed from database
    """
    return []

@unittest.mock.patch(target='src.database.db_controllers.user_session.execute')
@unittest.mock.patch(target='src.database.db_settings.update_configuration_file')
def test_dataset_loader(_, mocked_session):
    mocked_session.return_value = dataset
    created = db_manager.load_datasets(samples=10)
    assert isinstance(created, str)
    assert mocked_session.called_once()


def test_fail_databaset_loader():
    data = db_manager.load_datasets(samples=0)
    assert isinstance(data, pandas.DataFrame)
