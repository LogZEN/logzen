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

from logzen.db import Entity, JSONDict, DAO



class Stream(Entity):
    """ The database entity for streams.

        The filter defining the stream is stored as serialized JSON data in the
        entity.
    """

    __tablename__ = 'streams'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           nullable=False,
                           autoincrement=True)

    user_id = sqlalchemy.Column(sqlalchemy.ForeignKey('users.id'))

    user = sqlalchemy.orm.relationship('User')

    name = sqlalchemy.Column(sqlalchemy.Unicode,
                             nullable=False)

    description = sqlalchemy.Column(sqlalchemy.UnicodeText,
                                    nullable=False,
                                    default='')

    filter = sqlalchemy.Column(JSONDict,
                               nullable=False)



@export()
class Streams(DAO):
    """ DAO for accessing stream entities.
    """

    def getStream(self, name):
        try:
            return self.session \
                .query(Stream) \
                .filter(Stream.name == name) \
                .one()

        except sqlalchemy.orm.exc.NoResultFound:
            raise KeyError(name)


    def getStreams(self):
        """ Returns an iterator over all existing stream entities.
        """

        return iter(self.session.query(Stream))


    def createStream(self, name):
        """ Create a new stream entity.

            All parameters are passed as-is to the entity to create. The
            created entity is attached to the session and returned.
        """

        stream = Stream(name=name)

        self.session.add(stream)

        return stream
