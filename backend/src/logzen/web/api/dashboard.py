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

import uuid
import bottle

from logzen.web.api import resource


dashboard = {
    str(uuid.uuid4()): {'col': 1, 'row': 1, 'size_x': 2, 'size_y': 2, 'type': 'latestevents', 'title': 'c11', 'config': {}},
    str(uuid.uuid4()): {'col': 2, 'row': 1, 'size_x': 1, 'size_y': 2, 'type': 'latestevents', 'title': 'c21', 'config': {}},
    str(uuid.uuid4()): {'col': 3, 'row': 1, 'size_x': 1, 'size_y': 1, 'type': 'latestevents', 'title': 'c31', 'config': {}},
    str(uuid.uuid4()): {'col': 4, 'row': 1, 'size_x': 3, 'size_y': 1, 'type': 'latestevents', 'title': 'c41', 'config': {}},
    str(uuid.uuid4()): {'col': 1, 'row': 2, 'size_x': 2, 'size_y': 2, 'type': 'latestevents', 'title': 'c12', 'config': {}},
    str(uuid.uuid4()): {'col': 2, 'row': 2, 'size_x': 1, 'size_y': 1, 'type': 'latestevents', 'title': 'c22', 'config': {}},
    str(uuid.uuid4()): {'col': 3, 'row': 2, 'size_x': 1, 'size_y': 1, 'type': 'latestevents', 'title': 'c32', 'config': {}},
    str(uuid.uuid4()): {'col': 4, 'row': 2, 'size_x': 1, 'size_y': 1, 'type': 'latestevents', 'title': 'c42', 'config': {}},
    str(uuid.uuid4()): {'col': 2, 'row': 3, 'size_x': 1, 'size_y': 1, 'type': 'latestevents', 'title': 'c23', 'config': {}},
    str(uuid.uuid4()): {'col': 3, 'row': 3, 'size_x': 1, 'size_y': 1, 'type': 'latestevents', 'title': 'c33', 'config': {}},
    str(uuid.uuid4()): {'col': 6, 'row': 3, 'size_x': 2, 'size_y': 1, 'type': 'latestevents', 'title': 'c63', 'config': {}}
}


@resource('/dashboard', 'GET')
def get():
    return dashboard


@resource('/dashboard', 'POST')
def create():
    dashboard[uuid.uuid4()] = bottle.request.body


@resource('/dashboard/<id>', 'DELETE')
def delete(id):
    del dashboard[id]


@resource('/dashboard/<id>', 'PUT')
def update(id):
    dashboard[id] = bottle.request.body
