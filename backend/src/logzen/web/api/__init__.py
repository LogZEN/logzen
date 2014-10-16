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

from logzen.db import session
from logzen.users import Users

import bottle

import itsdangerous

import functools



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
             methods='GET',
             arg_request=None,
             arg_response=None,
             arg_session=None):
    @require(api='logzen.web.api:Api',
             logger='logzen.util:Logger')
    def extender(func,
                 api, logger):
        logger.debug('Register API resource: %s %s -> %s',
                     path, methods, func)

        # Wrap the function into the session decorator
        func = session(arg_session)(func)

        # Inject the request and response object
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if arg_request is not None:
                kwargs[arg_request] = bottle.request

            if arg_response is not None:
                kwargs[arg_response] = bottle.response

            # Call the decorated function
            return func(*args,
                        **kwargs)

        return api.route(path, methods, wrapper)
    return extender



@export()
class Signer():
    def __init__(self):
        self.__serializer = itsdangerous.TimedJSONWebSignatureSerializer('abc', 300)


    def sign(self, username):
        return self.__serializer.dumps(username).decode('ascii')


    def verify(self, token):
        try:
            return self.__serializer.loads(token.encode('ascii'))

        except itsdangerous.BadData:
            return None



TOKEN_COOKIE = 'logzen.auth'



@require(signer='logzen.web.api:Signer',
         logger='logzen.util:Logger')
@session(arg='db')
def before_request_hook(db, signer, logger):
    users = Users(db)

    # Ensure the user extension exists
    bottle.request.user = None

    # Get the token from the request
    token = bottle.request.get_cookie(TOKEN_COOKIE)

    # Check if the token is included in the request
    if token is None:
        logger.debug('No token found - unauthorized')

        # Nothing to do, if the token is missing
        return

    # Verify the token and extract the username
    username = signer.verify(token)
    if username is None:
        raise bottle.HTTPError(401, 'Invalid token')

    logger.debug('Token validated with username: %s', username)

    # Get the user object for the username
    user = users.getUser(username=username)
    if user is None:
        raise bottle.HTTPError(401, 'User does not exist: ' + username)

    logger.debug('User entry found: %s', user)

    # Inject the user into the request
    bottle.request.user = user



@require(signer='logzen.web.api:Signer',
         logger='logzen.util:Logger')
def after_request_hook(signer, logger):
    # Nothing to do if the request does not contain a user
    if bottle.request.user is None:
        logger.debug('No user entry attached to request - unauthorized')

        # Delete the token on the client
        bottle.response.delete_cookie(TOKEN_COOKIE)

    else:
        # Get the username from the request
        username = bottle.request.user.username

        logger.debug('Token generated for username: %s', username)

        # Generate the token by signing the username
        token = signer.sign(username)

        # Pass the token to the client
        bottle.response.set_cookie(TOKEN_COOKIE, token)



@extend('logzen.web.api:Api')
def auth_hook(api):
    # Add the token managing hooks to the API application
    api.add_hook('before_request', before_request_hook)
    api.add_hook('after_request', after_request_hook)



@resource('/token', 'POST',
          arg_session='db',
          arg_request='request')
def login(request,
          db):
    users = Users(db)

    user = users.getVerifiedUser(username=request.json['username'],
                                 password=request.json['password'])
    if user is None:
        raise bottle.HTTPError(401, 'Wrong username or password')

    # Set the user to the request - letting the after-request hook do the signing
    request.user = user

    # Return the users data
    return {'username': user.username}



@resource('/token', 'DELETE')
def logout(request):
    # Reset the user in the request - letting the after-request hook skip the signing
    request.user = None



def restricted(arg=None):
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            # Return 'not authorized', if the request is not authorized
            if bottle.request.user is None:
                raise bottle.HTTPError(401, 'Authentication required')

            # Inject the user into the wrapped function
            if arg is not None:
                kwargs[arg] = bottle.request.user

            # Call the decorated function
            return func(*args,
                        **kwargs)

        return wrapped
    return wrapper
