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

from logview.authentication.auth import AuthController

from logview.config import Config
from logview.settings import Settings
from logview.overview import Overview
from logview.events import Events


if __name__ == '__main__':
    dispatcher = cherrypy.dispatch.RoutesDispatcher()
    dispatcher.connect('overview1', '/', Overview(), action = 'index')
    dispatcher.connect('overview2', '/overview/events_by_host', Overview(), action = "get_events_by_host")
    dispatcher.connect('overview3', '/overview/top_hosts', Overview(), action = "get_top_hosts")
    dispatcher.connect('overview4', '/overview/new_events', Overview(), action = "get_new_events")
    dispatcher.connect('overview5', '/overview/severity_by_host', Overview(), action = "get_severity_by_host")
    dispatcher.connect('overview6', '/overview/program_by_host', Overview(), action = "get_program_by_host")

    dispatcher.connect('events1', '/events', Events(), action = 'index')
    dispatcher.connect('events2', '/events/update', Events(), action = 'update')
    dispatcher.connect('events3', '/events/tooltip', Events(), action = 'tooltip')

    dispatcher.connect('event1', '/event/event_details', Events(), action = 'get_event_details')
    dispatcher.connect('event2', '/event/similar_events', Events(), action = 'get_similar_events')
    dispatcher.connect('event3', '/event/similar_events_history', Events(), action = 'get_similar_events_history')
    dispatcher.connect('event4', '/event/:event_id', Events(), action = 'details')

    dispatcher.connect('settings1', '/settings/users/create', Settings(), action = 'user_create')

    dispatcher.connect('auth1', '/auth/login', AuthController(), action = 'login')
    dispatcher.connect('auth2', '/auth/logout', AuthController(), action = 'logout')


    config = {
        '/': {
            'request.dispatch': dispatcher,
            'tools.sessions.on': True
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
