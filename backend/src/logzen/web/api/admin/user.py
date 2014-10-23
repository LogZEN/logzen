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
    return {user.id: {'username': user.username}
            for user
            in users.getUsers()}


@resource('/users/<name>', 'GET')
@require(users='logzen.db.users:Users',
         request='logzen.web.api:Request')
def get(name,
        users,
        request):
    try:
        user = users.getUser(name)

        return {'id': user.id,
                'username': user.username,
                'admin': user.admin}

    except KeyError:
        raise bottle.HTTPError(404, 'User not found: %s' % name)

    return stream.query(request.body)


@resource('/users/<name>', 'PUT')
@require(users='logzen.db.users:Users',
         request='logzen.web.api:Request')
def delete(name,
           users,
           request):
    try:
        user = users.getUser(name)

    except KeyError:
        raise bottle.HTTPError(404, 'User not found: %s' % name)

    with session():
        user.__init__(**request.json)


@resource('/users/<name>', 'DELETE')
@require(users='logzen.db.users:Users')
def delete(name,
           users):
    with session():
        users.deleteUser(name)


@resource('/users', 'POST')
@require(users='logzen.db.users:Users',
         request='logzen.web.api:Request')
def create(users,
           request):
    with session():
        users.createUser(**request.json)

