'''
Copyright 2012 Sven Reissmann <sven@0x80.io>

This file is part of pyLogView.

pyLogView is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published
by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.

pyLogView is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with pyLogView.  If not, see <http://www.gnu.org/licenses/>.
'''

import datetime
import cherrypy

from logview.backends import backend

from logview import templates


class Overview:
    def __init__(self):
        pass

    @cherrypy.expose
    def index(self):
        template = templates.get_template('overview.html')
        return template.render()

    @cherrypy.expose
    def get_data(self,
              start = '1970-01-01 00:00:00',
              end = datetime.datetime.now()):
        template = templates.get_template('overview.ajax.html')

        d = backend.event_count_by_time(start, end)
        return template.render(d = d)
