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

import hashlib

from logview.config import Config
from logview import templates


class Help:
  def __init__(self):
    pass

  #=============================================================================
  # about
  #=============================================================================
  def about(self):
    template = templates.get_template('about.html')
    return template.render(pagename = "help")

  #=============================================================================
  # an information page shown for unconfigured installations
  #=============================================================================
  def unconfigured(self):
    template = templates.get_template('unconfigured.html')
    return template.render(pagename = "help")

  #=============================================================================
  # create user form
  #=============================================================================
  def user_create(self,
                  username = None,
                  password = None,
                  backlink = 0):
    template = templates.get_template('create_user.html')
    error_msg = ""
    configsection = None

    if username is None or password is None:
      pass

    elif username == "" or password == "":
      error_msg = "Please set a username and password"

    else:
      if Config().has_section(username):
        error_msg = '''
          The username you choose already exists in your configuration file.
          <br />Please be aware that usernames must be unique.
        '''

      configsection = {'username': username,
                       'password': hashlib.sha256(password).hexdigest()}

    return template.render(pagename = "create",
                           error_msg = error_msg,
                           backlink = backlink,
                           configsection = configsection)
