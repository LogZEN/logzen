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
from logzen.web.api.user import resource



@resource('/logs/*', ['GET', 'POST'])
@require(user='logzen.web.api.auth:User',
         request='logzen.web.api:Request',
         logs='logzen.logs:Logs')
def query(user,
          request,
          logs):
    return logs.queryWithUser(user=user,
                              query=request.json)



@resource('/logs/<stream>', ['GET', 'POST'])
@require(user='logzen.web.api.auth:User',
         request='logzen.web.api:Request',
         logs='logzen.logs:Logs')
def query(stream,
          user,
          request,
          logs):
    try:
        stream = user.streams[stream]

    except KeyError:
        raise bottle.HTTPError(404, 'Stream not found: %s' % stream)

    return logs.queryWithStream(stream=stream,
                                query=request.json)
