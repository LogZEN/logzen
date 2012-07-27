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
import math

import cherrypy

from logview.backends import backend
from logview import templates


class Events:
    def __init__(self):
        pass


    @cherrypy.expose
    def __call__(self,
             page = 0):
        return templates.get_template('eventlist.html').render()


    @cherrypy.expose
    def details(self,
                event_id):
        template = templates.get_template('event.html')

        event = backend.get_event(event_id)
        return template.render(event = event)


    @cherrypy.expose
    @cherrypy.tools.json_out()
    def update(self,
               page = 0,
               pagesize = 50,
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


        # message count by timeperiod
        countmap = []
        eventcount = backend.event_count_by_time(filters, steps)
        for c in eventcount:
            countmap.append({"time": str(c['time']), "count": c['count']})

        # event data
        eventmap = []
        events = backend.get_events(filters)
        numevents = events.get_count()
        if numevents > 0:
            for event in events.get_rows(int(page) * pagesize, pagesize):
                event['reported_time'] = str(event['reported_time'])
                event['received_time'] = str(event['received_time'])
                event['id'] = str(event['id'])
                eventmap.append(event)

        # define some metadata
        metadata = {}
        metadata['page'] = int(page)
        metadata['maxpages'] = math.ceil(numevents / pagesize)
        metadata['event_count'] = numevents
        metadata['event_first'] = str(int(page) * pagesize + 1)
        if (int(page) * pagesize + pagesize) > numevents:
            metadata['event_last'] = numevents
        else:
            metadata['event_last'] = int(page) * pagesize + pagesize

        metadata['zoom'] = level
        metadata['maxtime'] = str(filters['end_time'])

        return {"metadata": metadata,
                "eventcount": countmap,
                "events": eventmap}


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
