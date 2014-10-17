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


from require import require, singleton

import logzen.users
import logzen.streams

import logzen.web.frontend
import logzen.web.api
import logzen.web.api.db
import logzen.web.api.auth
import logzen.web.api.dashboard
import logzen.web.api.streams

from logzen.users import User
from logzen.streams import Stream



@require(app='logzen.web:App',
         session='logzen.db:Session')
def main(app,
         session):
    if session \
            .query(User) \
            .count() < 1:
        user = User(username='admin',
                    password='admin',
                    filter={ 'match_all' : {}})
        session.add(user)

        stream = Stream(name='everything',
                        user=user,
                        filter={ 'match_all' : {}})
        session.add(stream)

    session.commit()

    app.run()

#   dispatcher = cherrypy.dispatch.RoutesDispatcher()
#
#   dispatcher.connect('overview1', '/', Page(), action = 'index')
#
#   dispatcher.connect('api_query', '/_api/query', Api(), action = 'query')
#   dispatcher.connect('api_get', '/_api/get', Api(), action = 'get')
#
#   dispatcher.connect('config_widget', '/_api/config', Page(), action = 'get_config')
#   dispatcher.connect('config_layout', '/_api/config/dashboard', Page(), action = 'get_dashboard')
#
#   dispatcher.connect('login', '/_api/auth/login', AuthController(), action = 'login')
#   dispatcher.connect('logout', '/_api/auth/logout', AuthController(), action = 'logout')
#   dispatcher.connect('loggedin', '/_api/auth/getlogin', AuthController(), action = 'getlogin')
#
#   dispatcher.connect('tooltip_ip', '/_api/tooltip/ip', Page(), action = 'get_ip_tooltip')
#
#
#   config = {
#     '/': {
#       'request.dispatch': dispatcher,
#       'tools.caching.on': False,
#       'tools.sessions.on': True,
#       'tools.staticdir.on': True,
#       'tools.staticdir.section': '/',
#       'tools.staticdir.root': os.getcwd(),
#       'tools.staticdir.dir': 'web/build',
#     }
#   }
#   cherrypy.config.update('config/cherrypy.conf')
#   cherrypy.tree.mount(root = None, config = config)
#
# #  cherrypy.engine.subscribe('start_thread', xdb.connect)
#   cherrypy.engine.start()
#   cherrypy.engine.block()



if __name__ == '__main__':
    main()
