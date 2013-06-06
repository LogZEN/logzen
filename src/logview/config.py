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

from ConfigParser import SafeConfigParser


DEFAULTS = {'backend.minconn': '1',
            'backend.maxconn': '20',
            'backend.port': '5432',
            'ui.searchengine': 'google'
            }



class Config(object):
  __instance = None


  def __new__(cls, *args, **kwargs):
    if cls.__instance is None:
      cls.__instance = object.__new__(cls)
      cls.__instance.__init()

    return cls.__instance


  def __init(self):
    self.__parser = SafeConfigParser(DEFAULTS)

    config_files = ['config/logview.conf',
                    'config/users.conf']

    config_found = self.__parser.read(config_files)
    config_missing = set(config_files) - set(config_found)

    if len(config_missing) is not 0:
      print "Warning: Missing configuration files: %s" % config_missing


  def __getattr__(self,
                  section):
    parser = self.__parser

    class SectionWrapper():
      def __init__(self):
        pass

      def __getitem__(self, option):
        return parser.get(section, option)

      def __iter__(self):
        return iter(parser.items(section))

    return SectionWrapper()


  def has_section(self,
                  section):
    return self.__parser.has_section(section)


  def get(self,
          section,
          option):
    return self.__parser.get(section, option)
