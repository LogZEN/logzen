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

import socket
import datetime
import humanize

import cherrypy

from logview.backends import backend

from logview import templates

class Events:
    def __init__(self):
        pass

    @cherrypy.expose
    def list(self,
             page = 0):
        template = templates.get_template('eventlist.html')

        events = backend.get_events()
        return template.render(events = events,
                               page = int(page),
                               pagesize = 50)

    @cherrypy.expose
    def details(self,
                event_id):
        template = templates.get_template('event.html')

        event = backend.get_event(event_id)
        return template.render(event = event)

        pass

    @cherrypy.expose
    def filter(self,
               page = 0,
               host = None,
               facility = None,
               severity = None,
               program = None,
               message = None):
        template = templates.get_template('eventlist.ajax.html')

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

        events = backend.get_events(filters)
        return template.render(events = events,
                               page = int(page),
                               pagesize = 50)

    @cherrypy.expose
    def tooltip(self,
                event_id):
        template = templates.get_template('tooltip.ajax.html')

        event = backend.get_event(event_id)

        try:
            event['ip'] = socket.gethostbyname(event['host'])
        except:
            event['ip'] = 'Unknown'

        event['ago_time'] = humanize.naturaltime(datetime.datetime.now() - event['reported_time'])

        return template.render(event = event)
