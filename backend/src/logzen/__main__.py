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


from require import require, singleton

import logzen.web.frontend
import logzen.web.api
import logzen.web.api.db
import logzen.web.api.auth
import logzen.web.api.dashboard
import logzen.web.api.streams
import logzen.web.api.logs
import logzen.web.api.user
import logzen.web.api.admin
import logzen.web.api.admin.user

from logzen.db.users import User
from logzen.db.streams import Stream


@require(app='logzen.web:App',
         session='logzen.db:Session')
def main(app,
         session):
    if session \
            .query(User) \
            .count() < 1:
        admin = User(username='admin',
                     password='admin',
                     admin=True,
                     filter={ 'match_all' : {}})
        session.add(admin)

        user = User(username='user',
                    password='user',
                    filter={ 'match_all' : {}})
        session.add(user)

        stream = Stream(name='everything',
                        user=user,
                        filter={ 'match_all' : {}})
        session.add(stream)

    session.commit()

    app.run()


if __name__ == '__main__':
    main()
