


from require import *


@extend('logzen.config:ConfigFile')
def TestConfigFile(file):
    from configparser import ConfigParser

    config_file = ConfigParser()
    config_file.add_section('db')
    config_file.add_section('es')
    config_file.add_section('auth')
    config_file.add_section('log')

    config_file.set('db', 'url', 'sqlite:///')
    config_file.set('es', 'hosts', '')
    config_file.set('log', 'level', 'DEBUG')

    return config_file



@export(engine='logzen.db:Engine')
def TestConnection(engine):
    return engine.connect()



@extend('logzen.db:SessionFactory',
        connection='util:TestConnection')
def TestSessionFactory(factory,
                       connection):
    factory.configure(bind=connection)
