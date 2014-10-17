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
    impl = sqlalchemy.Text


    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)


    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)



@export()
def Engine():
    engine = sqlalchemy.create_engine('sqlite:///',
                                      pool_size=20,
                                      echo=True)

    # Create / update the schema
    Entity.metadata.create_all(engine)

    return engine


@export(engine='logzen.db:Engine')
def Sessions(engine):
    sessions = sqlalchemy.orm.sessionmaker()
    sessions.configure(bind=engine)

    return sessions



@export(oneshot,
        sessions='logzen.db:Sessions')
def Session(sessions):
    return sessions()



@contextlib.contextmanager
@require(session='logzen.db:Session')
def session(session):
    try:
        yield session

    except:
        session.rollback()
        raise

    else:
        session.commit()

    finally:
        session.close()


# def session(arg=None):
#     @require(session='logzen.db:Session')
#     def wrapper(func,
#                 session):
#         @functools.wraps(func)
#         def wrapped(*args, **kwargs):
#
#             # Pass the session to the wrapped function as an keyword argument
#             if arg is not None:
#                 kwargs[arg] = session
#
#             # Call the wrapped function
#             try:
#                 return func(*args,
#                             **kwargs)
#
#             except:
#                 session.rollback()
#                 raise
#
#             else:
#                 session.commit()
#
#             finally:
#                 session.close()
#
#         return wrapped
#     return wrapper
