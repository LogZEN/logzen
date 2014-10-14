from require import export

import logging




@export()
def Logger():
    logging.basicConfig(level=logging.DEBUG)

    return logging.getLogger('logzen')
