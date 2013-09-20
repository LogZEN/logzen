'''
Copyright 2013 Sven Reissmann <sven@0x80.io>

This file is part of LogZen.

LogZen is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

LogZen is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
for more details.

You should have received a copy of the GNU General Public License
along with LogZen. If not, see <http://www.gnu.org/licenses/>.
'''

import cherrypy

import os

from logzen.authentication.auth import AuthController

from logzen.db import Db
from logzen.page import Page
from logzen.api import Api



if __name__ == '__main__':
  dispatcher = cherrypy.dispatch.RoutesDispatcher()

  dispatcher.connect('overview1', '/', Page(), action = 'index')

  dispatcher.connect('api_query', '/_api/query', Api(), action = 'query')
  dispatcher.connect('api_get', '/_api/get', Api(), action = 'get')

  dispatcher.connect('config_widget', '/_config/get', Page(), action = 'get_config_option')
  dispatcher.connect('config_widget', '/_config/dashboard/layout', Page(), action = 'get_dashboard_layout')
  dispatcher.connect('config_widget', '/_config/dashboard/config', Page(), action = 'get_dashboard_config')

  dispatcher.connect('login', '/_auth/login', AuthController(), action = 'login')
  dispatcher.connect('logout', '/_auth/logout', AuthController(), action = 'logout')
  dispatcher.connect('loggedin', '/_auth/getlogin', AuthController(), action = 'getlogin')

  dispatcher.connect('tooltip_ip', '/_tooltip/ip', Page(), action = 'get_ip_tooltip')


  config = {
    '/': {
      'request.dispatch': dispatcher,
      'tools.sessions.on': True,
      'tools.staticdir.on': True,
      'tools.staticdir.section': '/',
      'tools.staticdir.root': os.getcwd(),
      'tools.staticdir.dir': 'web',
    }
  }
  cherrypy.config.update('config/cherrypy.conf')
  cherrypy.tree.mount(root = None, config = config)

#  cherrypy.engine.subscribe('start_thread', db.connect)
  cherrypy.engine.start()
  cherrypy.engine.block()
