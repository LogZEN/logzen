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

from logzen.web.api import resource

import bottle

import itsdangerous

import functools



TOKEN_COOKIE = 'logzen.auth'
TOKEN_DURATION = 300



@export()
class AuthPlugin():
    logger = require('logzen.util:Logger')

    users = require('logzen.users:Users')


    def __init__(self):
        self.__serializer = itsdangerous.TimedJSONWebSignatureSerializer('abc', TOKEN_DURATION)


    def __sign(self, username):
        return self.__serializer.dumps(username).decode('ascii')


    def __verify(self, token):
        try:
            return self.__serializer.loads(token.encode('ascii'))

        except itsdangerous.BadData:
            return None


    def apply(self, callback, route):
        def wrapper(*args, **kwargs):
            # Get the token from the request
            token = bottle.request.get_cookie(TOKEN_COOKIE)

            # Check if the token is included in the request
            if token is None:
                self.logger.debug('No token found - not authorized')

            else:
                # Verify the token and extract the username
                username = self.__verify(token)
                if username is None:
                    raise bottle.HTTPError(401, 'Invalid token')

                self.logger.debug('Token validated with username: %s', username)

                # Get the user object for the username
                user = self.users.getUser(username=username)
                if user is None:
                    raise bottle.HTTPError(401, 'User does not exist: ' + username)

                self.logger.debug('User entry found: %s', user)

                setattr(bottle.local, 'user', user)

            # Call the original route
            body = callback(*args, **kwargs)

            # Get the user object after the real request handler
            user = getattr(bottle.local, 'user', None)

            # Nothing to do if the request does not contain a user
            if user is None:
                self.logger.debug('No user entry attached to request - unauthorized')

                # Delete the token on the client
                bottle.response.delete_cookie(TOKEN_COOKIE,
                                              path='/api/v1')

            else:
                # Generate the token by signing the username
                token = self.__sign(user.username)

                self.logger.debug('Token generated for username: %s', user.username)

                # Pass the token to the client
                bottle.response.set_cookie(name=TOKEN_COOKIE,
                                           value=token,
                                           path='/api/v1',
                                           max_age=TOKEN_DURATION)

            return body

        return wrapper



@extend('logzen.web.api:Api',
        auth='logzen.web.api.auth:AuthPlugin')
def install(api,
            auth):
    api.install(auth)



@resource('/token', 'POST')
@require(request='logzen.web.api:Request',
         users='logzen.users:Users')
def login(request,
          users):
    user = users.getVerifiedUser(username=request.json['username'],
                                 password=request.json['password'])
    if user is None:
        raise bottle.HTTPError(401, 'Wrong username or password')

    # Set the user to the request - letting the after-request hook do the signing
    setattr(bottle.local, 'user', user)



@resource('/token', 'DELETE')
def logout():
    # Reset the user in the request - letting the after-request hook skip the signing
    delattr(bottle.local, 'user')



@export(oneshot)
def User():
    return getattr(bottle.local, 'user', None)



def restricted():
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            # Raise error, if the request is not authorized
            if getattr(bottle.local, 'user', None) is None:
                raise bottle.HTTPError(401, 'Authentication required')

            # Call the decorated function
            return func(*args,
                        **kwargs)

        return wrapped
    return wrapper
