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

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.types
import sqlalchemy.schema

from require import *
from logzen.db import Entity, JSONDict



class Stream(Entity):
    __tablename__ = 'streams'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           nullable=False,
                           autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('users.id'))

    user = sqlalchemy.orm.relationship('User')

    name = sqlalchemy.Column(sqlalchemy.String,
                             nullable=False)

    description = sqlalchemy.Column(sqlalchemy.Text,
                                    nullable=False,
                                    default='')

    filter = sqlalchemy.Column(JSONDict,
                               nullable=False)


    @require(es='logzen.es:Connection')
    def query(self, query, es):
        body = {}

        # Add the user filter and the stream filter to the search
        body.update({
            'filter': {
                'and': [
                    self.filter,
                    self.user.filter
                ]
            }
        })

        # Add the passed query - if any
        if query:
            body.update({
                'query': query
            })

        # Execute the search
        return es.search(body)



class Streams(object):
    def __init__(self, session):
        self.__session = session


    def getStream(self, name):
        try:
            return self.__session \
                .query(Stream) \
                .filter(Stream.name == name) \
                .one()

        except sqlalchemy.orm.exc.NoResultFound:
            raise KeyError(name)


    def getStreams(self):
        return iter(self.__session.query(Stream))


    def createStream(self, name):
        self.__session.add(Stream(name=name))
