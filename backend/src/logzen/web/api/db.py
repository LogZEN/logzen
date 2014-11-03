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

import sqlalchemy.orm



@extend('logzen.db:SessionFactory')
def RequestSessionFactory(factory):
    """ Extend the session factory to return a session for each request.
    """

    return sqlalchemy.orm.scoped_session(factory,
                                         lambda: bottle.request)



@export()
class SessionPlugin(object):
    """ A bottle plugin assigning a session for each request.

        For each request, a sqlalchemy session is acquired and attached to the
        request. After the request has finished, the session is released.
    """
    api = 2

    sessionFactory = require('logzen.db:SessionFactory')

    def apply(self, callback, route):
        def wrapper(*args, **kwargs):
            session = self.sessionFactory()
            setattr(bottle.local, 'session', session)

            try:
                return callback(*args, **kwargs)

            finally:
                delattr(bottle.local, 'session')
                self.sessionFactory.remove()

        return wrapper



@extend('logzen.web.api:Api',
        session='logzen.web.api.db:SessionPlugin',
        logger='logzen.util:Logger')
def install(api,
            session,
            logger):
    """ Installs the session plugin to the API.
    """

    api.install(session)

    logger.debug('Plugin "session" installed')
