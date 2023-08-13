import logging 


def setup_logging():
    logging.basicConfig(
        format='%(asctime)s %(levelname)s | %(name)s | %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S'
    )
