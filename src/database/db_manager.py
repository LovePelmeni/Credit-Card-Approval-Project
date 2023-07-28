import db_settings
import pandas
import click 
import constants
import logging
import sql_requests
import os

user_session = db_settings.get_user_session()

if os.environ.get("TESTING_MODE", 1) == 0:
    Logger = logging.getLogger(__name__)
    file_handler = logging.FileHandler(filename="../../logs/db_settings.log")
    Logger.addHandler(file_handler)
else:
    Logger = logging.getLogger(__name__)


@click.command()
@click.option("--samples", type=int, help="number of samples to load")
def load_datasets(samples: int):
    """
    Function provides CLI interfaces for extracting and loading data from database 
    using Clustered-based sampling technique. 
    
    Args:
        n_groups: int - number of groups (clusters) to load

    Example:
        $ db_manager load_datasets --groups 5
    """
    if samples == 0: return "Pass valid number of samples! Zero is not allowed"
    try:
        query_data = user_session.execute(
            sql_requests.DATASET_LOAD_REQUEST, {'samples': samples}
        ).fetchall()

        if len(query_data) == 0:
            raise SystemExit(
                "\n\n Your database is empty. Add some data \n\n"
            )

        df = pandas.DataFrame(query_data)
        credit_transactions = df[constants.TRANSACTION_TABLE_FIELDS]
        credit_applications = df[constants.APPLICATION_TABLE_FIELDS]
        save_datasets(credit_applications, credit_transactions)
        raise SystemExit(
            "\n\n%s samples has been loaded and saved inside `raw_data` directory!\n\n"
        )

    except Exception as exc:
        Logger.error(exc)
        raise SystemExit("\n\nFailed to load data, check logs\n\n")

def save_datasets(applications: pandas.DataFrame, transactions: pandas.DataFrame):
    """
    Function saves Credit Applications and Credit Transactions datasets 
    to local
    """
    applications.to_csv(constants.APPLICATION_DATASET_PATH)
    transactions.to_csv(constants.TRANSACTION_DATASET_PATH)



if __name__ == '__main__':
    load_datasets()