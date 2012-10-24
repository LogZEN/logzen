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

import pyes

from logview.config import Config


class ElasticSearchBackend:
    def __init__(self):
        servers = [value for key, value in Config().es if key.startswith('server_')]

        self.__connection = pyes.ES(servers)

    def query(self,
              query):
        return self.__connection.search_raw(query = query,
                                            indices = Config().es['index'],
                                            doc_types = Config().es['type'])

    def get(self,
            id):
        return self.__connection.get(id = id,
                                     index = Config().es['index'],
                                     doc_type = Config().es['type'],)

backend = ElasticSearchBackend()
