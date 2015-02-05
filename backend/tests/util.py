from require import *
from require.mock import *



@mock('logzen.config:ConfigFile')
def mockConfigFile(file):
    from configparser import ConfigParser

    config_file = ConfigParser()
    config_file.add_section('db')
    config_file.add_section('es')
    config_file.add_section('auth')
    config_file.add_section('log')

    config_file.set('db', 'url', 'sqlite:///')
    config_file.set('es', 'hosts', '')
    config_file.set('log', 'level', 'DEBUG')

    file.return_value = config_file



@mock('logzen.es:Connection')
def mockElasticsearch(connection):
    connection.return_value.search.side_effect = lambda request: request



@export(engine='logzen.db:Engine')
def TestConnection(engine):
    return engine.connect()



@extend('logzen.db:SessionFactory',
        connection='util:TestConnection')
def TestSessionFactory(factory,
                       connection):
    factory.configure(bind=connection)
