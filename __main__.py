import cherrypy

import os

from logview.overview import Overview
from logview.events import Events


if __name__ == '__main__':

    dispatcher = cherrypy.dispatch.RoutesDispatcher()
    dispatcher.connect('overview', '/', Overview())

    dispatcher.connect('events', '/events', Events(), action = 'list')
    dispatcher.connect('events', '/events/:event_id', Events(), action = 'details')
    dispatcher.connect('events', '/events/filter/:type/:value', Events(), action = 'filter')

    # Create CherryPy server
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
