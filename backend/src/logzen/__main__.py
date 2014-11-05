"""
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
"""

from require import require, extend

from logzen.db.users import User
from logzen.db.streams import Stream


@extend('logzen.config:ConfigDecl')
def BottleConfigDecl(config_decl):
    with config_decl('wsgi') as section_decl:

        # The ip address to listen on
        section_decl('host',
                     default='127.0.0.1')
        # The tcp port to listen on
        section_decl('port',
                     default=8080)


@require(app='logzen.web:App',
         session='logzen.db:Session',
         users='logzen.db.users:Users',
         config='logzen.config:Config')
def main(app,
         session,
         users,
         config):
    if session \
            .query(User) \
            .count() < 1:
        admin = users.createUser(username='admin',
                                 password='admin',
                                 admin=True)
        admin.streams.set(Stream(name='everything',
                                 filter={'match_all': {}}))

        user = users.createUser(username='user',
                                password='user')
        user.streams.set(Stream(name='everything',
                                filter={'match_all': {}}))

    session.commit()

    app.run(host=config.wsgi.host,
            port=config.wsgi.port)


if __name__ == '__main__':
    main()
