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

import cherrypy

from logzen.config import Config
from logzen.authentication.auth import require



class Page:
  _cp_config = {
    'tools.auth.on': True
  }


  def __init__(self):
    pass


  def index(self):
    return open(os.path.join('web', u'index.html'))


  @require()
  @cherrypy.tools.json_out()
  def get_widget_config(self):
    return [{
             'id': 1,
             'size': 8,
             'widget': [ 'latestevents' ]
             },
             {
             'id': 2,
             'size': 4,
             'widget': [ 'topevents', 'tophosts' ]
             }
             ]


  @cherrypy.tools.json_out()
  def get_config_option(self,
                           section,
                           option):
    return {
            'section': section,
            'option': option,
            'value': Config().get(section, option)
            }
