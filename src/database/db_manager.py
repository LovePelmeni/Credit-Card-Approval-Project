import db_settings, pandas
import click 
from src.offline_training import constants
import logging

user_session = db_settings.get_user_session()
Logger = logging.getLogger(__name__)

file_handler = logging.FileHandler(filename="logs/db_manager.log")
Logger.addHandler(file_handler)

sql_request = """
    with randomized_applications as (
        select *
        from CustomerApplications order by random()
    ),
    samples as (
        select * from randomized_applications limit :samples
    )
    
    select * from samples s join CreditTransactions c 
    on s.client_id = c.customer_id
"""

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
            sql_request, {'samples': samples}
        ).fetchall()

        df = pandas.DataFrame(query_data)
        credit_transactions = df[constants.CREDIT_TRANSACTIONS_FIELDS]
        credit_applications = df[constants.CREDIT_APPLICATIONS_FIELDS]
        save_datasets(credit_applications, credit_transactions)
    except Exception as exc:
        Logger.error(exc)

def save_datasets(applications: pandas.DataFrame, transactions: pandas.DataFrame):
    """
    Function saves Credit Applications and Credit Transactions datasets 
    to local
    """
    applications.to_csv(constants.APPLICATION_DATASET_PATH)
    transactions.to_csv(constants.TRANSACTION_DATASET_PATH)



if __name__ == '__main__':
    load_datasets()