from require import *

import logging


@extend('logzen.config:ConfigDecl')
def LoggerConfigDecl(config_decl):
    with config_decl('log') as section_decl:
        # The log level to produce
        section_decl('level',
                     default=logging.INFO)


@export(config='logzen.config:Config')
def Logger(config):
    """ Configure logging and return a logger.
    """

    logging.basicConfig(level=config.log.level)

    logging.getLogger('logzen').setLevel(level=config.log.level)

    logging.getLogger('sqlalchemy').setLevel(level=config.log.level)
    logging.getLogger('sqlalchemy.engine').setLevel(level=config.log.level)
    logging.getLogger('sqlalchemy.pool').setLevel(level=config.log.level)
    logging.getLogger('sqlalchemy.orm').setLevel(level=config.log.level)

    return logging.getLogger('logzen')
