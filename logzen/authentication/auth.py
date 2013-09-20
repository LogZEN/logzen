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

import hashlib

from logzen.config import Config


SESSION_KEY = Config().logzen['sessionkey']



def check_credentials(username, password):
  ''' Verify credentials for username and password
  '''
  if Config().has_section(username):
    if Config().get(username, 'password') == hashlib.sha256(password).hexdigest():
      return None

  return u"Incorrect username or password."


def check_auth(*args, **kwargs):
  ''' Search the config for 'auth.require'. If found and not None, 
      a login is required, meaning, a username must exist in SESSION_KEY
      variable. If not, redirect to index page. 
  '''
  conditions = cherrypy.request.config.get('auth.require', None)
  if conditions is not None:
    username = cherrypy.session.get(SESSION_KEY)
    if username:
      cherrypy.request.login = username
    else:
      raise cherrypy.HTTPRedirect("/")

cherrypy.tools.auth = cherrypy.Tool('before_handler', check_auth)



def require(*conditions):
  ''' Decorator that appends conditions to the auth.require config variable
  '''
  def decorate(func):
    if not hasattr(func, '_cp_config'):
      func._cp_config = dict()

    if 'auth.require' not in func._cp_config:
      func._cp_config['auth.require'] = []

    func._cp_config['auth.require'].extend(conditions)
    return func

  return decorate


class AuthController(object):
  @cherrypy.tools.json_out()
  def login(self,
            username = None,
            password = None):
    if username is None or password is None:
      return {
              'success': 'false',
              'message': 'Username or password not provided.'
              }

    error_msg = check_credentials(username, password)
    if error_msg:
      return {
              'success': 'false',
              'message': error_msg
              }

    else:
      cherrypy.session.regenerate()
      cherrypy.session[SESSION_KEY] = cherrypy.request.login = username

      return {
              'success': 'true',
              'message': 'Authenticated as ' + username + '.'
              }


  @cherrypy.tools.json_out()
  def logout(self):
    username = cherrypy.session.get(SESSION_KEY, None)
    cherrypy.session[SESSION_KEY] = None

    if username:
      cherrypy.request.login = None

    return {
            'success': 'true',
            'message': 'Logged out.'
            }


  @cherrypy.tools.json_out()
  def getlogin(self):
    username = cherrypy.session.get(SESSION_KEY)
    return {
            'success': username != None,
            'username': username
            }
