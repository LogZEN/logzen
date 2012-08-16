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
import urllib

from logview import templates
from logview.config import Config


SESSION_KEY = Config().logview['sessionkey']

def check_credentials(username, password):
  if Config().has_section(username):
    if Config().get(username, 'password') == hashlib.sha256(password).hexdigest():
      return None

  return u"Incorrect username or password."

def check_auth(*args, **kwargs):
  get_parmas = urllib.quote(cherrypy.request.request_line.split()[1])
  username = cherrypy.session.get(SESSION_KEY)
  if username:
    cherrypy.request.login = username
  else:
    raise cherrypy.HTTPRedirect("/auth/login?from_page=%s" % get_parmas)

cherrypy.tools.auth = cherrypy.Tool('before_handler', check_auth)

def require(func = None):
  def decorate(func):
    if not hasattr(func, '_cp_config'):
      func._cp_config = dict()
    if 'auth.require' not in func._cp_config:
      func._cp_config['auth.require'] = []
    return func

  return decorate


class AuthController(object):
  @cherrypy.expose
  def login(self,
            username = None,
            password = None,
            from_page = "/"):
    template = templates.get_template('login.html')

    if username is None or password is None:
      return template.render(pagename = "login",
                             from_page = from_page)

    error_msg = check_credentials(username, password)
    if error_msg:
      return template.render(pagename = "login",
                             username = username,
                             error_msg = error_msg,
                             from_page = from_page)

    else:
      cherrypy.session.regenerate()
      cherrypy.session[SESSION_KEY] = cherrypy.request.login = username
      raise cherrypy.HTTPRedirect(from_page or "/")


  @cherrypy.expose
  def logout(self,
             from_page = "/"):
    username = cherrypy.session.get(SESSION_KEY, None)
    cherrypy.session[SESSION_KEY] = None

    if username:
      cherrypy.request.login = None

    raise cherrypy.HTTPRedirect(from_page or "/")
