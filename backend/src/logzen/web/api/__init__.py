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



@export(app='logzen.web:App')
def Api(app):
    # Generate a new bottle application containing the API
    api = bottle.Bottle()

    # Avoid fancy error pages for the API
    api.default_error_handler = lambda res: str(res.body)

    # Mount the API application to the root application
    app.mount('/api/v1',
              api)

    return api



def resource(path,
             methods='GET'):
    @require(api='logzen.web.api:Api',
             logger='logzen.util:Logger')
    def extender(func,
                 api,
                 logger):
        logger.debug('Register API resource: %s %s -> %s',
                     path, methods, func)

        return api.route(path, methods, func)
    return extender



@export(oneshot)
def Request():
    return bottle.request



@export(oneshot)
def Response():
    return bottle.response

