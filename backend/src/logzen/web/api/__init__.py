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
    @require(logger='logzen.util:Logger')
    def error_handler(response,
                      logger):
        logger.error('Error occurred: %s - %s',
                     response.status_line,
                     response.exception)

        # Return the error message as response
        return str(response.body)

    api.default_error_handler = error_handler

    # Mount the API application to the root application
    app.mount('/api/v1',
              api)

    return api



def resource(path,
             method='GET',
             **config):
    @require(api='logzen.web.api:Api',
             logger='logzen.util:Logger')
    def extender(func,
                 api,
                 logger):
        logger.debug('Register API resource: %s %s -> %s',
                     path, method, func)

        return api.route(path, method, func, **config)
    return extender



@export(oneshot)
def Request():
    return bottle.request



@export(oneshot)
def Response():
    return bottle.response



import logzen.web.api.db
import logzen.web.api.schema
import logzen.web.api.auth
import logzen.web.api.user
import logzen.web.api.admin
