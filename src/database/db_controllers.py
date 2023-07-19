import db_settings, pandas 
from src.modeling import constants

user_session = db_settings.get_user_session()
important_features = ','.join(constants.IMPORTANT_FEATURES)

stratify_records = (
    lambda number_of_samples: """
    with categories as (
        select distinct bad as status_category
        from CreditTransactions
    ),
    records as (
        select 
            row_number() over(partition by status_category order by rand() ) as rnk,
            *
        from CustomerApplications as app_recs 
        join CreditTransactions as credit_recs using(client_id)
    )
    select * from records where rnk <= %s

""" % (
    number_of_samples
    )
)

def get_records_dataset(
    samples_per_category: int
):
    """
    Function parses unified records (application + credit history record) data 
    from database using Stratify Sampling Strategy
    Args:
        samples_per_category: number of samples per category 
    Returns:
        pandas.DataFrame object with loaded data 
    """
    if samples_per_category <= 0: 
        raise ValueError("Invalid Number of Samples passed, should be greater than 0")
    try:
        records = stratify_records(samples_per_category)
        data = user_session.execute(statement=records)
        return pandas.DataFrame(data=data)

    except(RuntimeError):
        raise NotImplemented