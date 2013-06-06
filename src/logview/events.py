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

from logview.authentication.auth import require
from logview.geoip import geoip
from logview import templates



class Events:
  _cp_config = {
    'tools.auth.on': True
  }


  def __init__(self):
    pass


  #=============================================================================
  # eventlist
  #=============================================================================
  @require()
  def index(self):
    template = templates.get_template('eventlist.html')
    return template.render(pagename = "events")


  #=============================================================================
  # eventlist - live
  #=============================================================================
  @require()
  def live(self):
    template = templates.get_template('eventlist_live.html')
    return template.render(pagename = "live")


  #=============================================================================
  # event details page
  #=============================================================================
  @require()
  def details(self,
              event_id):
    template = templates.get_template('event.html')
    return template.render(pagename = "event",
                           event_id = event_id)
