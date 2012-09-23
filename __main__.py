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
from logview.help import Help
from logview.overview import Overview
from logview.events import Events
from logview.tooltips import Tooltips
from logview.api import Api


if __name__ == '__main__':
  dispatcher = cherrypy.dispatch.RoutesDispatcher()

  if Config().logview['configured'] != "True":
    dispatcher.connect('overview1', '/', Help(), action = 'unconfigured')
    dispatcher.connect('help2', '/help/create_user', Help(), action = 'user_create')

  else:
    dispatcher.connect('overview1', '/', Overview(), action = 'index')
    dispatcher.connect('events1', '/events', Events(), action = 'index')
    dispatcher.connect('event4', '/event/:event_id', Events(), action = 'details')

    dispatcher.connect('tooltips1', '/tooltips/event', Tooltips(), action = 'event')
    dispatcher.connect('tooltips2', '/tooltips/ip', Tooltips(), action = 'ip_address')

    dispatcher.connect('help1', '/help/about', Help(), action = 'about')
    dispatcher.connect('help2', '/help/create_user', Help(), action = 'user_create')

    dispatcher.connect('auth1', '/auth/login', AuthController(), action = 'login')
    dispatcher.connect('auth2', '/auth/logout', AuthController(), action = 'logout')

    dispatcher.connect('query', '/_api/query', Api(), action = 'query')

  config = {
    '/': {
      'request.dispatch': dispatcher,
      'tools.sessions.on': True
    },
    '/static' : {
      'tools.staticdir.on': True,
      'tools.staticdir.section': '/static',
      'tools.staticdir.root': os.getcwd(),
      'tools.staticdir.dir': 'web',
    }
  }
  cherrypy.config.update('config/cherrypy.conf')
  cherrypy.tree.mount(root = None, config = config)

  cherrypy.engine.start()
  cherrypy.engine.block()
