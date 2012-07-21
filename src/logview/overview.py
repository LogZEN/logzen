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
                 host = None,
                 facility = None,
                 severity = None,
                 program = None,
                 message = None,
                 start_time = '1970-01-01 00:00:00',
                 end_time = datetime.datetime.now()):

        filters = {}
        if host is not None:
            filters['host'] = '%' + host + '%'
        if facility is not None:
            filters['facility'] = '%' + facility + '%'
        if severity is not None:
            filters['severity'] = '%' + severity + '%'
        if program is not None:
            filters['program'] = '%' + program + '%'
        if message is not None:
            filters['message'] = '%' + message + '%'

        filters['start_time'] = start_time
        filters['end_time'] = end_time

        eventcount = backend.event_count_by_time(filters)

        template = templates.get_template('overview.ajax.html')
        return template.render(eventcount = eventcount)
