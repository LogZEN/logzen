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

import humanize

from datetime import datetime, timedelta

from logview.authentication.auth import require
from logview.backend import backend
from logview import templates



class Overview:
  _cp_config = {
    'tools.auth.on': True
  }


  def __init__(self):
    pass


  #=============================================================================
  # dashboard
  #=============================================================================
  @require()
  def index(self):
    template = templates.get_template('overview.html')
    return template.render(pagename = "overview")


  @cherrypy.tools.json_out()
  @require()
  def get_events_by_host(self):
    events_by_host = backend.event_count_by_host()
    return events_by_host


  @cherrypy.tools.json_out()
  @require()
  def get_top_hosts(self,
                    timerange = 1):
    starttime = datetime.now() - timedelta(days = int(timerange))
    top_hosts = backend.event_peaks(starttime)

    data = {}
    data['data'] = top_hosts
    data['metadata'] = {"timerange": timerange}

    return data


  @cherrypy.tools.json_out()
  @require()
  def get_new_events(self,
                     filters = 7):
    eventmap = []
    events = backend.new_events(filters = int(filters))
    for event in events:
      event['reported_time'] = humanize.naturaltime(datetime.now() - event['reported_time'])
      eventmap.append(event)

    return eventmap


  @cherrypy.tools.json_out()
  @require()
  def get_severity_by_host(self,
                           host = None):
    if host == "":
      host = None

    data = {}
    eventmap = {}
    events = backend.get_severity_count(host)
    if events > 0:
      s = 0
      for event in events:
        s += event['count']
        eventmap[event['severity']] = event['count']
      eventmap['sum'] = s

    data['count_severity'] = eventmap
    data['hosts'] = backend.get_hosts()
    return data


  @cherrypy.tools.json_out()
  @require()
  def get_program_by_host(self,
                          host):
    if host == "":
      host = None

    data = {}
    eventmap = {}
    events = backend.get_program_count(host)
    if events > 0:
      s = 0
      for event in events:
        s += event['count']
        eventmap[event['program']] = event['count']
      eventmap['sum'] = s

    data['count_program'] = eventmap
    data['hosts'] = backend.get_hosts()
    return data
