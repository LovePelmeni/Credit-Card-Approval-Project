from sqlalchemy import text

DATASET_LOAD_REQUEST = text(
"""
    with randomized_applications as (
        select * from applications order by random()
    ), 
    selected_samples as (
        select * from randomized_applications limit :samples
    )
    select * from applications;
"""
)

