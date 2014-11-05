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



@extend('logzen.config:ConfigDecl')
def ElasticsearchConfigDecl(config_decl):
    with config_decl('es') as section_decl:
        # The hosts running elasticsearch
        section_decl('hosts')

        # The username / password used to authenticate on the elasticsearch
        # cluster
        section_decl('username',
                     default=None)
        section_decl('password',
                     default=None)

        # The index containing the syslog messages
        section_decl('index',
                     default='syslog')



@export()
class Connection:
    """ Connection to ElasticSearch.

        Creates a (pooled) low-level connection to the ElasticSearch cluster.
    """

    logger = require('logzen.util:Logger')

    config = require('logzen.config:Config')


    def __init__(self):
        if self.config.es.username and self.config.es.password:
            auth = (self.config.es.username,
                    self.config.es.password)

        else:
            auth = None

        self.__connection = Elasticsearch(self.config.es.host,
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
                                        index=self.config.es.index)
