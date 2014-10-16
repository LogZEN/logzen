from require import export

import logging



try:
    from inspect import signature
except:
    from funcsigs import signature



@export()
def Logger():
    logging.basicConfig(level=logging.DEBUG)

    return logging.getLogger('logzen')
