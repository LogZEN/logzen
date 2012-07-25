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
        return template.render()

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
               message = None,
               start_time = '1970-01-01 00:00:00',
               end_time = datetime.datetime.now()):
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

        filters['start_time'] = start_time
        filters['end_time'] = end_time

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

    @cherrypy.expose
    def get_event_count(self,
                 host = None,
                 facility = None,
                 severity = None,
                 program = None,
                 message = None,
                 start_time = None,
                 end_time = None):

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

        if start_time is None:
            filters['start_time'], filters['end_time'] = backend.event_timestamp_range()
        else:
            filters['start_time'] = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            filters['end_time'] = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')

        interval = filters['end_time'] - filters['start_time']

        steps = 'second'
        level = 5
        if interval.total_seconds() > 120:
            steps = 'minute'
            level = 4
        if interval.total_seconds() > 7200:        # 60 * 60 * 2
            steps = 'hour'
            level = 3
        if interval.total_seconds() > 345600:      # 60 * 60 * 24 * 4
            steps = 'day'
            level = 2
        if interval.total_seconds() > 7776000:     # 60 * 60 * 24 * 90
            steps = 'month'
            level = 1
        if interval.total_seconds() > 31536000:    # 60 * 60 * 24 * 365
            steps = 'year'
            level = 0

        print steps
        eventcount = backend.event_count_by_time(filters,
                                                 steps)

        template = templates.get_template('overview.ajax.html')
        return template.render(eventcount = eventcount,
                               zoomlevel = level,
                               maxtime = filters['end_time'])
