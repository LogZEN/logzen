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
    """ A bottle plugin creating a session for each request.

        For each incoming request, a sqlalchemy session is created and attached
        to the requests.
    """

    sessionFactory = require('logzen.db:SessionFactory')

    def apply(self, callback, route):
        def wrapper(*args, **kwargs):
            setattr(bottle.local, 'session', self.sessionFactory())

            return callback(*args, **kwargs)

        return wrapper



@extend('logzen.web.api:Api',
        session='logzen.web.api.db:SessionPlugin')
def install(api,
            session):
    """ Installs the session plugin to the API.
    """

    api.install(session)



@extend('logzen.db:SessionProvider')
def RequestSessionProvider(base):
    """ Extension providing the request session if it exists.

        The extension provides the request specific session created by the
        bottle plugin above. If no such session exists (i.e. not called in a
        bottle request context), the base provider is returned.
    """

    if hasattr(bottle.local, 'session'):
        return lambda: getattr(bottle.local, 'session')

    else:
        return base
