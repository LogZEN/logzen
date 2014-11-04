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

from logzen.web.api import resource as api_resource
from logzen.web.api.auth import restricted


def resource(path,
             method='GET',
             **config):
    def wrapper(func):
        return api_resource('/admin' + path,
                            method,
                            **config)(restricted(func,
                                                 lambda user: user is not None and user.admin))

    return wrapper


import logzen.web.api.admin.users
