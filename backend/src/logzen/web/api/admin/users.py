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

import bottle

from require import *
from logzen.web.api.admin import resource
from logzen.db import session


@resource('/users', 'GET')
@require(users='logzen.db.users:Users')
def list(users):
    return {user.username: {'username': user.username,
                            'admin': user.admin}
            for user
            in users.getUsers()}


@resource('/users/<name>', 'GET')
@require(users='logzen.db.users:Users')
def get(name,
        users):
    try:
        user = users.getUser(name)

        return {'username': user.username,
                'admin': user.admin}

    except KeyError:
        raise bottle.HTTPError(404, 'User not found: %s' % name)


@resource('/users', 'POST',
          schema={'type': 'object',
                  'properties': {'username': {'type': 'string'},
                                 'password': {'type': 'string'},
                                 'admin': {'type': 'boolean'}},
                  'required': ['username',
                               'password']})
@require(users='logzen.db.users:Users',
         request='logzen.web.api:Request')
def create(users,
           request):
    with session():
        users.createUser(**request.data)


@resource('/users/<name>', 'PUT',
          schema={'type': 'object',
                  'properties': {'username': {'type': 'string'},
                                 'password': {'type': 'string'},
                                 'admin': {'type': 'boolean'}},
                  'required': ['username',
                               'password']})
@require(users='logzen.db.users:Users',
         request='logzen.web.api:Request')
def update(name,
           users,
           request):
    with session():
        try:
            user = users.getUser(name)
            user.__init__(**request.data)

        except KeyError:
            raise bottle.HTTPError(404, 'User not found: %s' % name)


@resource('/users/<name>', 'DELETE')
@require(users='logzen.db.users:Users')
def delete(name,
           users):
    with session():
        try:
            user = users.getUser(name)
            users.deleteUser(user)

        except KeyError:
            raise bottle.HTTPError(404, 'User not found: %s' % name)

