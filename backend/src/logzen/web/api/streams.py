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

from logzen.streams import Streams
from logzen.web.api import resource, restricted



@resource('/streams', 'GET')
@restricted()
def list(db):
    streams = Streams(db)

    return [{'name': stream.name,
             'description': stream.description}
            for stream
            in streams]


@resource('/streams/<name>', 'GET')
@restricted()
def get(name,
        db):
    streams = Streams(db)

    try:
        stream = streams(name)

        return {'name': stream.name,
                'description': stream.description,
                'masks': [{'title': mask.title,
                           'query': mask.query}
                          for mask
                          in stream.masks]}

    except KeyError:
        raise bottle.HTTPError(404, 'Stream not found: %s' % name)

    return stream.query(bottle.request.body)


@resource('/streams/<name>', 'POST')
@restricted()
def query(name,
          db):
    streams = Streams(db)

    try:
        stream = streams(name)

    except KeyError:
        raise bottle.HTTPError(404, 'Stream not found: %s' % name)

    return {'and': [
        {'or': [mask.query
                for mask
                in stream.masks
                if mask.active]},
        bottle.request.body
    ]}
