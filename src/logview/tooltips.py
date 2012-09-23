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

import socket
import humanize
import string

from datetime import datetime

from logview.authentication.auth import require
from logview.backend import backend
from logview.geoip import geoip
from logview import templates
from logview.config import Config


class Tooltips:
  _cp_config = {
    'tools.auth.on': True
  }

  def __init__(self):
    templates.globals['searchengine'] = Config().logview['ui.searchengine']

  #=============================================================================
  # event tooltip
  #=============================================================================
  @require()
  def event(self,
            event_id):
    template = templates.get_template('tooltip.event.html')

    event = backend.get_event(event_id)

    try:
      event['ip'] = socket.gethostbyname(event['host'])
    except:
      event['ip'] = 'Unknown'

    event['ago_time'] = humanize.naturaltime(datetime.now() - event['reported_time'])

    return template.render(event = event)

  #=============================================================================
  # ip address tooltip
  #=============================================================================
  @require()
  def ip_address(self,
                 ip):
    template = templates.get_template('tooltip.ip.html')

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

    return template.render(data = data)
