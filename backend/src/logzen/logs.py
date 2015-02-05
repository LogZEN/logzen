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


@export()
class Logs(object):
    """ Service for accessing logs.
    """

    MATCH_ALL = {'match_all': {}}

    es = require('logzen.es:Connection')


    def queryWithFilter(self,
                        filter,
                        query=None):
        """ Search for logs using the passed filter and an optional query.
        """

        request = {}

        # Add the filter to the request - if any
        if filter:
            request['filter'] = filter

        # Add the query to the request - if any
        if query:
            request['query'] = query

        else:
            request['query'] = self.MATCH_ALL

        # Execute the request
        result = self.es.search(request)

        return result


    def queryWithFilters(self,
                         filters,
                         query=None):
        """ Search for logs using the passed filters and an optional query.

            If the filters does contain more than one filter, the filters are concatinated using the 'and' operation.
        """

        # Add the filters to the request
        if not filters:
            # Do not use a filter
            filter = None

        elif len(filters) == 1:
            # Use the single filter as-is
            filter = filters[0]

        else:
            # Concatenate all filters using 'and' operation
            filter = {'and': filters}

        # Execute the query
        return self.queryWithFilter(filter,
                                    query)


    def queryWithUser(self,
                      user,
                      query=None):
        """ Search for logs using the passed users filter and an optional query.
        """

        return self.queryWithFilter(user.filter,
                                    query)


    def queryWithStream(self,
                        stream,
                        query=None):
        """ Search for logs using the passed streams filter and an optional query.
        """

        filters = []

        # Add the user filter to the list of filters - if any
        if stream.user.filter:
            filters.append(stream.user.filter)

        # Add the stream filter to the list of filters - if any
        if stream.filter:
            filters.append(stream.filter)

        return self.queryWithFilters(filters,
                                     query)
