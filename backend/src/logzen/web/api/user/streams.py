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
from logzen.db import session
from logzen.web.api.user import resource


@resource('/streams', 'GET')
@require(user='logzen.web.api.auth:User',
         streams='logzen.db.streams:Streams')
def list(user,
         streams):
    return {stream.name: {'description': stream.description,
                          'filter': stream.filter}
            for stream
            in streams.getStreamsByUser(user)}


@resource('/streams/<name>', 'GET')
@require(user='logzen.web.api.auth:User',
         streams='logzen.db.streams:Streams')
def get(name,
        user,
        streams):
    try:
        stream = streams.getStreamByName(user, name)

    except KeyError:
        raise bottle.HTTPError(404, 'Stream not found: %s' % name)

    return {'name': stream.name,
            'description': stream.description,
            'filter': stream.filter}


@resource('/streams', 'POST',
          schema={'type': 'object',
                  'properties': {'name': {'type': 'string'},
                                 'description': {'type': 'string'},
                                 'filter': {'type': 'object'}},
                  'required': ['name',
                               'filter']})
@require(user='logzen.web.api.auth:User',
         streams='logzen.db.streams:Streams',
         request='logzen.web.api:Request')
def create(user,
           streams,
           request):
    with session():
        streams.createStream(user, **request.data)


@resource('/streams/<name>', 'PUT',
          schema={'type': 'object',
                  'properties': {'name': {'type': 'string'},
                                 'description': {'type': 'string'},
                                 'filter': {'type': 'object'}},
                  'required': ['name',
                               'filter']})
@require(user='logzen.web.api.auth:User',
         streams='logzen.db.streams:Streams',
         request='logzen.web.api:Request')
def update(name,
           user,
           streams,
           request):
    with session():
        try:
            stream = streams.getStreamByName(user, name)

        except KeyError:
            raise bottle.HTTPError(404, 'Stream not found: %s' % name)

        stream.__init__(**request.data)


@resource('/streams/<name>', 'DELETE')
@require(user='logzen.web.api.auth:User',
         streams='logzen.db.streams:Streams')
def delete(name,
           user,
           streams):
    with session():
        try:
            stream = streams.getStreamByName(user, name)

        except KeyError:
            raise bottle.HTTPError(404, 'Stream not found: %s' % name)

        streams.deleteStream(stream)

