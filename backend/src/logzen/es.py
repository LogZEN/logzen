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

from elasticsearch import Elasticsearch
from elasticsearch.connection import Urllib3HttpConnection
from elasticsearch.serializer import JSONSerializer

# from logzen.xconfig import config



@export()
class Connection:
    """ Connection to ElasticSearch.

        Creates a (pooled) low-level connection to the ElasticSearch cluster.
    """
    logger = require('logzen.util:Logger')


    def __init__(self):
        servers = ['localhost'] #[value for key, value in config.system.es if key.startswith('server_')]

        username = None #config.system.es['username']
        password = None #config.system.es['password']

        if username and password:
            auth = (username, password)

        else:
            auth = None

        self.__connection = Elasticsearch(servers,
                                          connection_class=Urllib3HttpConnection,
                                          http_auth=auth)

    def search(self,
               body):
        """ Execute a search query.

            The passed query must be a valid ElasticSearch query. This query is
            passed to the connection with the according index and the result is
            returned.
        """
        self.logger.debug('Execute search: %s',
                          JSONSerializer().dumps(body))

        return self.__connection.search(body=body,
                                        index='syslog') #config.system.es.index)


    def get(self,
            id):
        """ Fetches an document.

            The document with the passed id is fetched from the according index
            and is returned.
        """
        return self.__connection.get(id=id,
                                     index='syslog') #config.system.es.index)
