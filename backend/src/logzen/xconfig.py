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

from ConfigParser import SafeConfigParser


DEFAULTS = {'logzen.searchengine': 'ixquick'}



class SectionWrapper(object):
  def __init__(self, config, section):
    super(SectionWrapper, self).__setattr__('_config', config)
    super(SectionWrapper, self).__setattr__('_section', section)


  def __getattr__(self, option):
    return self[option]


  def __getitem__(self, option):
    return self._config._get_option(self._section, option)


  def __setattr__(self, option, value):
    self[option] = value


  def __setitem__(self, option, value):
    self._config._set_option(self._section, option, value)


  def __hasattr__(self, option):
    return option in self


  def __hasitem__(self, option, value):
    return self._config._has_option(self._section, option)


  def __iter__(self):
    return self._config._iter(self._section)



class ConfigWrapper(object):
  def __init__(self, path):
    self.__path = path

    self.__parser = SafeConfigParser(DEFAULTS)
    self.__parser.read(path)


  def __getattr__(self,
                  section):
    return self[section]

  def __getitem__(self,
                  section):
    return SectionWrapper(config = self,
                          section = section)


  def __hasattr__(self,
                  section):
    return section in self


  def __contains__(self,
                   section):
    return self.__parser.has_section(section)


  def add_section(self,
                  section):
    self.__parser.add_section(section)


  def _get_option(self,
                  section,
                  option):
    return self.__parser.get(section, option)


  def _set_option(self,
                  section,
                  option,
                  value):
    self.__parser.set(section, option, value)

    with open(self.__path, 'wb') as configfile:
      self.__parser.write(configfile)


  def _has_option(self,
                  section,
                  option):
    return self.__parser.has_option(section, option)


  def _iter(self,
            section):
    return iter(self.__parser.items(section))



class Config(object):
  def __init__(self):
    self.system = ConfigWrapper('config/logzen.conf')
    self.users = ConfigWrapper('config/users.conf')



config = Config()
