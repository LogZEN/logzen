from require import export

import logging



@export()
def Logger():
    """ Return a logger.
    """

    logging.basicConfig(level=logging.DEBUG)

    return logging.getLogger('logzen')
