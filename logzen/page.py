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

import os
import socket
import string

import cherrypy

from logzen.config import config
from logzen.geoip import geoip
from logzen.authentication.auth import require



class Page:
  _cp_config = {
    'tools.auth.on': True
  }


  def __init__(self):
    pass


  def index(self):
    return open(os.path.join('web', 'build', 'index.html'))


  @require()
  @cherrypy.tools.json_out()
  def get_dashboard(self):
    return [{"col": 1, "row": 1, "size_x": 2, "size_y": 2, "type": "latestevents", "title": "c11", "config": {}},
            {"col": 2, "row": 1, "size_x": 1, "size_y": 2, "type": "latestevents", "title": "c21", "config": {}},
            {"col": 3, "row": 1, "size_x": 1, "size_y": 1, "type": "latestevents", "title": "c31", "config": {}},
            {"col": 4, "row": 1, "size_x": 3, "size_y": 1, "type": "latestevents", "title": "c41", "config": {}},
            {"col": 1, "row": 2, "size_x": 2, "size_y": 2, "type": "latestevents", "title": "c12", "config": {}},
            {"col": 2, "row": 2, "size_x": 1, "size_y": 1, "type": "latestevents", "title": "c22", "config": {}},
            {"col": 3, "row": 2, "size_x": 1, "size_y": 1, "type": "latestevents", "title": "c32", "config": {}},
            {"col": 4, "row": 2, "size_x": 1, "size_y": 1, "type": "latestevents", "title": "c42", "config": {}},
            {"col": 2, "row": 3, "size_x": 1, "size_y": 1, "type": "latestevents", "title": "c23", "config": {}},
            {"col": 3, "row": 3, "size_x": 1, "size_y": 1, "type": "latestevents", "title": "c33", "config": {}},
            {"col": 6, "row": 3, "size_x": 2, "size_y": 1, "type": "latestevents", "title": "c63", "config": {}}
           ]



  @cherrypy.tools.json_out()
  def get_config(self,
                 key):
    return {'key': key,
            'value': config.system.logzen[key]}



  #
  # tooltip specific
  #
  @require()
  @cherrypy.tools.json_out()
  def get_ip_tooltip(self,
                     ip):

    data = {}
    data['ip'] = ip

    try:
      name, aliaslist, addresslist = socket.gethostbyaddr(ip)
      data['dns'] = name
      data['aliaslist'] = string.join(aliaslist, "<br />")
      data['addresslist'] = string.join(addresslist, "<br />")
    except:
      data['dns'] = "Unknown"
      data['aliaslist'] = ""
      data['addresslist'] = ""

    data['country'] = geoip.country(ip)
    data['flagimg'] = string.lower(data['country'])

    return data


