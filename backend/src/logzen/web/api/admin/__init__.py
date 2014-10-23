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
import functools



@export(api='logzen.web.api:Api')
def AdminApi(api):
    # Generate a new bottle application containing the API
    adminapi = bottle.Bottle()

    # Avoid fancy error pages for the API
    adminapi.default_error_handler = lambda res: str(res.body)

    # Mount the API application to the root application
    api.mount('/admin',
              adminapi)

    return adminapi


def resource(path,
             methods='GET'):
    @require(adminapi='logzen.web.api.admin:AdminApi',
             logger='logzen.util:Logger')
    def extender(func,
                 adminapi,
                 logger):
        logger.debug('Register Admin API resource: %s %s -> %s',
                     path, methods, func)

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            # Raise error, if the request is not authorized
            user = getattr(bottle.local, 'user', None)
            if user is None or not user.admin:
                raise bottle.HTTPError(401, 'Authentication required')

            # Call the decorated function
            return func(*args,
                        **kwargs)

        return adminapi.route(path, methods, wrapped)
    return extender

