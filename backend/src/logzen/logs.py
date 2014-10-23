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

    users = require('logzen.db.users:Users')
    streams = require('logzen.db.users:Streams')


    def query(self,
              stream,
              query=None):
        """ Search for logs using the passed stream and query.

            The returned log list is filtered by the filter assigned to the
            user owning the stream and by an optional filter assigned to a stream.

            The returned value is the unmodified result of the executed
            ElasticSearch query.
        """

        request = {
        }

        # Add the filters to the request
        if stream.user.filter and stream.filter:
            # Create a combined filter using the user filter and stream filter
            request.update({
                'filter': {
                    'and': [
                        stream.user.filter,
                        stream.filter
                    ]
                }
            })

        elif stream.user.filter:
            # Use only the user filter
            request.update({
                'filter': stream.user.filter
            })

        elif stream.filter is not None:
            # Use only the stream filter
            request.update({
                'filter': stream.filter
            })

        # Add the query to the request - if any
        if query:
            request.update({
                'query': query,
            })

        # Execute the search
        return self.es.search(request)
