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

from logview.overview import Overview
from logview.events import Events


if __name__ == '__main__':

    dispatcher = cherrypy.dispatch.RoutesDispatcher()
    dispatcher.connect('overview', '/', Overview(), action = 'index')
    dispatcher.connect('overview', '/overview/range', Overview(), action = 'get_data')

    dispatcher.connect('events', '/events', Events(), action = 'list')
    dispatcher.connect('events', '/events/filter', Events(), action = 'filter')
    dispatcher.connect('events', '/events/tooltip', Events(), action = 'tooltip')
    dispatcher.connect('events', '/event/:event_id', Events(), action = 'details')

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
    cherrypy.config.update('config/main.conf')
    cherrypy.tree.mount(root = None, config = config)

    cherrypy.engine.start()
    cherrypy.engine.block()
