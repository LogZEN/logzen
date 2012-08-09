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

import cherrypy

import os

from logview.config import Config
from logview.overview import Overview
from logview.events import Events


if __name__ == '__main__':
    dispatcher = cherrypy.dispatch.RoutesDispatcher()
    dispatcher.connect('overview', '/', Overview())
    dispatcher.connect('overview', '/overview/events_by_host', Overview(), action = "get_events_by_host")
    dispatcher.connect('overview', '/overview/top_hosts', Overview(), action = "get_top_hosts")
    dispatcher.connect('overview', '/overview/new_events', Overview(), action = "get_new_events")
    dispatcher.connect('overview', '/overview/severity_by_host', Overview(), action = "get_severity_by_host")
    dispatcher.connect('overview', '/overview/program_by_host', Overview(), action = "get_program_by_host")

    dispatcher.connect('events', '/events', Events())
    dispatcher.connect('events', '/events/update', Events(), action = 'update')
    dispatcher.connect('events', '/events/tooltip', Events(), action = 'tooltip')

    dispatcher.connect('event', '/event/event_details', Events(), action = 'get_event_details')
    dispatcher.connect('event', '/event/similar_events', Events(), action = 'get_similar_events')
    dispatcher.connect('event', '/event/similar_events_history', Events(), action = 'get_similar_events_history')
    dispatcher.connect('event', '/event/:event_id', Events(), action = 'details')

    config = {
        '/': {
              'request.dispatch': dispatcher
        },
        '/static' : {
            'tools.staticdir.on' : True,
            'tools.staticdir.section' : '/static',
            'tools.staticdir.root' : os.getcwd(),
            'tools.staticdir.dir' : 'resources',
        }
    }
    cherrypy.config.update('config/cherrypy.conf')
    cherrypy.tree.mount(root = None, config = config)

    cherrypy.engine.start()
    cherrypy.engine.block()
