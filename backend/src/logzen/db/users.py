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

from logzen.db import Entity, JSONDict, DAO

import sqlalchemy
import sqlalchemy.types
import sqlalchemy.orm.exc
from sqlalchemy.orm import validates

import hashlib


class Password(sqlalchemy.types.TypeDecorator):
    """ A sqlalchemy type wrapper storing an password in a secured.

        The password is hashed while setting the value. A 'decryption' is not
        possible.

        In addition to stored values, literals are hashed in the same way
        allowing comparison of passwords.
    """

    # TODO: Use passlib to store a salt

    impl = sqlalchemy.String

    def process_bind_param(self, value, dialect):
        if value is not None:
            return hashlib.sha512(value.encode('utf8')).hexdigest()


    def process_literal_param(self, value, dialect):
        if value is not None:
            return hashlib.sha512(value.encode('utf8')).hexdigest()


class User(Entity):
    """ Entity representing a user.
    """

    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           nullable=False,
                           autoincrement=True)

    username = sqlalchemy.Column(sqlalchemy.String,
                                 nullable=False,
                                 unique=True)

    password = sqlalchemy.Column(Password,
                                 nullable=False)

    admin = sqlalchemy.Column(sqlalchemy.Boolean,
                              default=False)

    filter = sqlalchemy.Column(JSONDict,
                               nullable=False)

    streams = sqlalchemy.orm.relationship('Stream',
                                          collection_class=sqlalchemy.orm.collections.attribute_mapped_collection('name'),
                                          cascade='all, delete-orphan')

    @validates('username')
    def validate_username(self, key, username):
        assert username

        return username

    @validates('password')
    def validate_password(self, key, password):
        assert len(password) >= 4

        return password


@export()
class Users(DAO):
    """ Accessor for user entities.
    """

    def getUser(self, username):
        """ Get a user entity with the given username.

            If a user with such username exists, the user entity is returned.
            If no such user exists, None is returned.
        """

        try:
            return self.session \
                    .query(User) \
                    .filter(User.username == username) \
                    .one()

        except sqlalchemy.orm.exc.NoResultFound:
            raise KeyError(username)


    def getVerifiedUser(self, username, password):
        """ Get a user entity with the given username and a matching password.

            If a user with such username exists and the users password matches
            the given one the user entity is returned - None otherwise.
        """
        try:
            return self.session \
                    .query(User) \
                    .filter(User.username == username, \
                            User.password == password) \
                    .one()

        except sqlalchemy.orm.exc.NoResultFound:
            return None


    def getUsers(self):
        return iter(self.session.query(User))


    def deleteUser(self, username):
        try:
            user = self.session \
                    .query(User) \
                    .filter(User.username == username) \
                    .one()

            self.session.delete(user)

        except sqlalchemy.orm.exc.ObjectDeletedError:
            raise KeyError(username)


    def createUser(self, **kwargs):
        try:
            user = User(**kwargs)
            self.session.add(user)

            return user

        except:
            raise
