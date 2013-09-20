'''
Copyright 2012 Sven Reissmann <sven@0x80.io>

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

from logzen.elasticsearch import es
from logzen.authentication.auth import require



class Api:
  _cp_config = {
    'tools.auth.on': True
  }


  def __init__(self):
    pass


  @require()
  @cherrypy.tools.json_in()
  @cherrypy.tools.json_out()
  def query(self):
    query = cherrypy.request.json
    try:
        return es.query(query)

    except Exception as e:
        cherrypy.response.status = "500 %s" % str(e)


  @require()
  @cherrypy.tools.json_out()
  def get(self, id):
    try:
        return es.get(id)

    except Exception as e:
        cherrypy.response.status = "500 %s" % str(e)
