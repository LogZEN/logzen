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

from logview.backends import backend

from logview import templates


class Overview:
    def __init__(self):
        pass

    @cherrypy.expose
    def __call__(self):
        template = templates.get_template('overview.html')

        return template.render(count = 100,
                               count_last_hour = 30,
                               count_this_hour = 42)
