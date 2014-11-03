'''
Copyright 2013 Sven Reissmann <sven@0x80.io>

This file is part of LogZen.

LogZen is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

LogZen is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
for more details.

You should have received a copy of the GNU General Public License
along with LogZen. If not, see <http://www.gnu.org/licenses/>.
'''

from require import *

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.declarative

import json

import contextlib


Entity = sqlalchemy.ext.declarative.declarative_base()



class JSONDict(sqlalchemy.types.TypeDecorator):
    """ A sqlalchemy type wrapper storing a python dict using JSON.

        This handler stores any kind of (nested) python dict in a single field
        by (de-)serializing the dict to a JSON object and stores it in a TEXT
        field.
    """

    impl = sqlalchemy.Text


    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)


    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)



@export()
def Engine():
    """ The sqlalchemy engine.

        The configured database is populated with the whole schema during
        initialisation.
    """

    # Create the engine instance
    engine = sqlalchemy.create_engine('sqlite:///',
                                      pool_size=20)

    # Create / update the schema
    Entity.metadata.create_all(engine)

    return engine



@export(engine='logzen.db:Engine')
def SessionFactory(engine):
    """ Returns the factory used to create new sessions.

        By default, a new session is created on each request.
    """

    return sqlalchemy.orm.sessionmaker(bind=engine)



@export(scope=oneshot,
        sessionFactory='logzen.db:SessionFactory')
def Session(sessionFactory):
    """ Returns a session.

        A session is acquired using the session factory on each request.
    """

    return sessionFactory()



@contextlib.contextmanager
@require(session='logzen.db:Session')
def session(session):
    """ A context manager for session handling.

        The context manager handles session creation, commit / rollback and
        closing in an appropriate way.
    """

    try:
        yield session

    except:
        session.rollback()
        raise

    else:
        session.commit()


class DAO(object):
    """ Base class for all DAOs.

        The base class provides the current session.
    """

    session = require('logzen.db:Session')
