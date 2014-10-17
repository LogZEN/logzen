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

import bottle



@export()
class SessionPlugin(object):
    sessions = require('logzen.db:Sessions')

    def apply(self, callback, route):
        def wrapper(*args, **kwargs):
            setattr(bottle.local, 'session', self.sessions())

            return callback(*args, **kwargs)

        return wrapper



@extend('logzen.web.api:Api',
        session='logzen.web.api.db:SessionPlugin')
def install(api,
            session):
    api.install(session)



@extend('logzen.db:Session')
def RequestSession(globalSession):
    if hasattr(bottle.local, 'session'):
        return getattr(bottle.local, 'session')

    else:
        return globalSession
