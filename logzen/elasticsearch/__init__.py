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

from elasticsearch import Elasticsearch
from elasticsearch.connection import Urllib3HttpConnection

from logzen.config import config


class ElasticSearch:
    def __init__(self):
        servers = [value for key, value in config.system.es if key.startswith('server_')]

        username = config.system.es['username']
        password = config.system.es['password']

        if username and password:
            auth = (username, password)

        else:
            auth = None

        self.__connection = Elasticsearch(servers,
                                          connection_class=Urllib3HttpConnection,
                                          http_auth=auth)

    def query(self,
              query):
        return self.__connection.search(body = query,
                                        index = config.system.es.index)


    def get(self,
            id):
        return self.__connection.get(id = id,
                                     index = config.system.es.index)

es = ElasticSearch()
