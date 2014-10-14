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

import sqlite3



class Db(object):
  def connect(self):
    if os.path.isfile('config/configuration.xdb') is not True:
      self.__connection = sqlite3.connect('config/configuration.xdb')
      self.__cursor = self.__connection.cursor()
      self.create()

    else:
      self.__connection = sqlite3.connect('config/configuration.xdb')
      self.__cursor = self.__connection.cursor()


  def create(self):
    ''' Create the initial database
    '''
    self.__cursor.execute('''CREATE TABLE config (key text, value text)''')
    self.__cursor.execute('''CREATE TABLE users (username text, password text)''')

    values = [('configured', 'false'),
              ('sessionkey', '_logzen_session'),
              ('ui.searchengine', 'ixquick')
              ]

    self.__cursor.executemany('INSERT INTO config VALUES (?, ?)', values)

    self.__connection.commit()


  def getConfig(self,
                key):
    ''' Get a key-value pair from the database
    '''
    self.__cursor.execute("SELECT value FROM config WHERE key = ?",
                          (key,))
    return self.__cursor.fetchone()[0]


  def getUser(self,
              username):
    ''' Get user information from the database
    '''
    self.__cursor.execute("SELECT username, password FROM users WHERE key = ?",
                          (username,))
    return self.__cursor.fetchone()


  def addUser(self,
               username,
               password):
    ''' Add a new user to the database
    '''
    self.__cursor.execute("SELECT username FROM users WHERE username = ?",
                          (username,))
    if self.__cursor.fetchone() is not None:
      self.__cursor.execute("INSERT INTO users VALUES (?, ?)",
                            (username, password,))


db = Db()
