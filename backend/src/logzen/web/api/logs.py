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
from logzen.web.api import resource
from logzen.web.api.auth import restricted



@resource('/logs/<stream>', ['GET', 'POST'])
@restricted()
@require(user='logzen.web.api.auth:User',
         request='logzen.web.api:Request',
         logs='logzen.logs:Logs')
def query(name,
          user,
          request,
          logs):
    # Resolve the stream entity
    try:
        stream = user.streams[name]

    except KeyError:
        raise bottle.HTTPError(404, 'Stream not found: %s' % name)

    # Execute the query and return the result
    return logs.query(stream=stream,
                      query=request.json)
