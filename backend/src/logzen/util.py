from require import export

import logging



@export()
def Logger():
    """ Configure logging and return a logger.
    """

    logging.basicConfig(level=logging.DEBUG)

    logging.getLogger('logzen').setLevel(level=logging.DEBUG)

    logging.getLogger('sqlalchemy').setLevel(level=logging.DEBUG)
    logging.getLogger('sqlalchemy.engine').setLevel(level=logging.DEBUG)
    logging.getLogger('sqlalchemy.pool').setLevel(level=logging.DEBUG)
    logging.getLogger('sqlalchemy.orm').setLevel(level=logging.DEBUG)

    return logging.getLogger('logzen')
