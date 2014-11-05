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

from require import *

from collections import namedtuple
from contextlib import contextmanager

import configparser

import bunch


ConfigOption = namedtuple('Option', ['conv',
                                     'default'])


@export()
class ConfigDecl(object):
    REQUIRED = object()

    def __init__(self):
        self.__sections = {}

        self.__materialized = False


    @contextmanager
    def __call__(self, section_name):
        # If the declaration is already materialized, no further extending is
        # possible
        assert not self.__materialized

        # Create a section declaration if it does not exists
        if section_name not in self.__sections:
            section = self.__sections[section_name] = {}
        else:
            section = self.__sections[section_name]

        # The option declaration function returned as the context
        def declarator(option_name,
                       conv=str,
                       default=self.REQUIRED):
            # Check if the section already contains the option
            if option_name in section:
                raise KeyError('Duplicated option declaration %s:%s' % (section_name, option_name))

            # Add the option to the section
            self.__sections[section_name][option_name] = ConfigOption(conv=conv,
                                                                      default=default)

        # Return the function as context
        yield declarator


    def materialize(self):
        """ Materialize the declarations.

            All section and option declarations collected are returned and
            further modification is prohibited.
        """

        self.__materialized = True

        return self.__sections


@export()
def ConfigFile():
    # Open and load the configuration file
    config_file = configparser.ConfigParser()
    config_file.read(filenames=('/etc/logzen.conf',
                                'logzen.conf'))

    return config_file


@export(config_decl='logzen.config:ConfigDecl',
        config_file='logzen.config:ConfigFile')
def Config(config_decl,
           config_file):

    # Build a config namespace
    config = bunch.Bunch()

    # Parse all declared sections
    for section_name, options in config_decl.materialize().items():
        # Build a section namespace
        section = bunch.Bunch()

        # Parse the options in the section
        for option_name, option in options.items():
            if config_file.has_option(section_name, option_name):
                # Option is declared in config files - load the raw value from
                # the config file
                raw_value = config_file.get(section_name,
                                            option_name)

                # Parse the value
                value = option.conv(raw_value)

            elif option.default != config_decl.REQUIRED:
                # Option is not declared but has a default
                if callable(option.default):
                    # If the default value is a function, evaluate it
                    value = option.default()
                else:
                    # Use the default as value as is
                    value = option.default

            else:
                # Value is required - throwing an exception
                raise KeyError('Missing option %s:%s' % (section_name, option_name))

            # Assign the option to the section namespace
            section[option_name] = value

        # Assign the section namespace to the config one
        config[section_name] = section

    return config


# from ConfigParser import SafeConfigParser
#
#
# DEFAULTS = {'logzen.searchengine': 'ixquick'}
#
#
#
# class SectionWrapper(object):
# def __init__(self, config, section):
#     super(SectionWrapper, self).__setattr__('_config', config)
#     super(SectionWrapper, self).__setattr__('_section', section)
#
#
#   def __getattr__(self, option):
#     return self[option]
#
#
#   def __getitem__(self, option):
#     return self._config._get_option(self._section, option)
#
#
#   def __setattr__(self, option, value):
#     self[option] = value
#
#
#   def __setitem__(self, option, value):
#     self._config._set_option(self._section, option, value)
#
#
#   def __hasattr__(self, option):
#     return option in self
#
#
#   def __hasitem__(self, option, value):
#     return self._config._has_option(self._section, option)
#
#
#   def __iter__(self):
#     return self._config._iter(self._section)
#
#
#
# class ConfigWrapper(object):
#   def __init__(self, path):
#     self.__path = path
#
#     self.__parser = SafeConfigParser(DEFAULTS)
#     self.__parser.read(path)
#
#
#   def __getattr__(self,
#                   section):
#     return self[section]
#
#   def __getitem__(self,
#                   section):
#     return SectionWrapper(config = self,
#                           section = section)
#
#
#   def __hasattr__(self,
#                   section):
#     return section in self
#
#
#   def __contains__(self,
#                    section):
#     return self.__parser.has_section(section)
#
#
#   def add_section(self,
#                   section):
#     self.__parser.add_section(section)
#
#
#   def _get_option(self,
#                   section,
#                   option):
#     return self.__parser.get(section, option)
#
#
#   def _set_option(self,
#                   section,
#                   option,
#                   value):
#     self.__parser.set(section, option, value)
#
#     with open(self.__path, 'wb') as configfile:
#       self.__parser.write(configfile)
#
#
#   def _has_option(self,
#                   section,
#                   option):
#     return self.__parser.has_option(section, option)
#
#
#   def _iter(self,
#             section):
#     return iter(self.__parser.items(section))
#
#
#
# class Config(object):
#   def __init__(self):
#     self.system = ConfigWrapper('config/logzen.conf')
#     self.users = ConfigWrapper('config/users.conf')
#
#
#
# config = Config()
