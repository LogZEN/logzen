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


from require import *

import logzen.users
import logzen.streams

import logzen.web.frontend
import logzen.web.api
import logzen.web.api.dashboard
import logzen.web.api.streams
import logzen.web.api.users

from logzen.users import User
from logzen.streams import Stream, Mask


@require(app='logzen.web:App',
         sessions='logzen.db:Sessions')
def main(app,
         sessions):
    session = sessions()

    if session \
            .query(User) \
            .count() < 1:
        admin = User(username='admin',
                     password='admin')
        session.add(admin)

    if session \
        .query(Stream) \
        .count() < 1:
        stream = Stream(name = 'everything')

        mask = Mask(title = 'Everything',
                    query = { 'match_all' : {}})
        stream.masks.append(mask)

        session.add(mask, stream)

    session.commit()

    app.run()


if __name__ == '__main__':
    main()
