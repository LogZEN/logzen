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

from abc import ABCMeta, abstractmethod

class Result:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_count(self):
        pass

    @abstractmethod
    def get_rows(self,
                 offset,
                 count):
        pass

class Backend:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_logs(self):
        pass