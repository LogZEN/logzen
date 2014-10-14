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
import sqlalchemy.types
import sqlalchemy.schema

import json

from logzen.db import Entity



class JSONDict(sqlalchemy.types.TypeDecorator):
    impl = sqlalchemy.Text


    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)


    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)



class Mask(Entity):
    __tablename__ = 'masks'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           nullable=False,
                           autoincrement=True)

    stream_id = sqlalchemy.Column(sqlalchemy.BigInteger,
                                  sqlalchemy.ForeignKey('streams.id'))

    title = sqlalchemy.Column(sqlalchemy.String,
                              nullable=False)

    query = sqlalchemy.Column(JSONDict,
                              nullable=False)

    active = sqlalchemy.Column(sqlalchemy.Boolean,
                               nullable=False,
                               default=True)



class Stream(Entity):
    __tablename__ = 'streams'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           nullable=False,
                           autoincrement=True)

    name = sqlalchemy.Column(sqlalchemy.String,
                             nullable=False)

    description = sqlalchemy.Column(sqlalchemy.Text,
                                    nullable=False,
                                    default='')

    masks = sqlalchemy.orm.relationship('Mask',
                                        backref='stream')



class Streams(object):
    def __init__(self, session):
        self.__session = session


    def __getitem__(self, name):
        try:
            return self.__session \
                    .query(Stream) \
                    .filter(Stream.name == name) \
                    .one()

        except sqlalchemy.orm.exc.NoResultFound:
            raise KeyError(name)


    def __iter__(self):
        return iter(self.__session.query(Stream))


    def create(self, name):
        self.__session.add(Stream(name=name))
