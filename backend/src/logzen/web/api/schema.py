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

import io
import json

import bottle
import jsonschema

from require import *


@export()
class SchemaPlugin():
    api = 2

    logger = require('logzen.util:Logger')


    def apply(self, callback, route):
        # Return unmodified callback if no schema is defined
        if not 'schema' in route.config:
            return callback

        # Extract the schema
        schema = route.config['schema']

        # Build a validator
        validator = jsonschema.Draft4Validator(schema=schema)

        # Build the wrapper verifying the schema
        def wrapper(*args, **kwargs):
            try:
                # Parse the request body to JSON
                body = io.TextIOWrapper(bottle.request.body,
                                        errors='strict',
                                        encoding='utf8')
                bottle.request.data = json.load(body)

                # Validate the request data against the schema
                validator.validate(bottle.request.data)

            except (ValueError, jsonschema.ValidationError) as error:
                # If validation failed - respond with appropriate return code
                raise bottle.HTTPError(status=400,
                                       body='Malformed data')

            else:
                # If validation succeeds - call the callback
                return callback(*args, **kwargs)

        return wrapper


@extend('logzen.web.api:Api',
        auth='logzen.web.api.schema:SchemaPlugin')
def install(api,
            auth):
    api.install(auth)
