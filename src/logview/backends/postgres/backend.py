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

import collections

import psycopg2.pool
import psycopg2.extras

from logview.backends.backend import Backend, Result


class PostgresResult:
    def __init__(self,
                 connection_pool,
                 filters):
        self.__connection_pool = connection_pool

        self.__connection = self.__connection_pool.getconn()
        self.__cursor = self.__connection.cursor()

        sql = '''
            SELECT *
            FROM events
            WHERE host LIKE COALESCE(%(host)s, host)
              AND facility LIKE COALESCE(%(facility)s, facility)
              AND severity LIKE COALESCE(%(severity)s, severity)
              AND program LIKE COALESCE(%(program)s, program)
              AND message LIKE COALESCE(%(message)s, message)
            ORDER BY reported_time DESC;
        '''

        self.__cursor.execute(sql, collections.defaultdict(lambda: None, filters))

    def __del__(self):
        self.__connection_pool.putconn(self.__connection)

    def get_count(self):
        return self.__cursor.rowcount

    def get_rows(self,
                 offset,
                 count):
        self.__cursor.scroll(value = offset,
                             mode = 'absolute')
        return self.__cursor.fetchmany(size = count)


class PostgresBackend:
    def __init__(self):
        self.__connection_pool = psycopg2.pool.ThreadedConnectionPool(minconn = 1,
                                                                      maxconn = 20,
                                                                      host = '127.0.0.1',
                                                                      port = 5432,
                                                                      database = 'syslog',
                                                                      user = 'syslog',
                                                                      password = 'd2u33fG9aC',
                                                                      connection_factory = psycopg2.extras.RealDictConnection)

    def __del__(self):
        self.__connection_pool.closeall()

    def get_events(self,
                   filters = {}):
        return PostgresResult(self.__connection_pool,
                              filters)

    def get_event(self,
                 event_id):
        connection = self.__connection_pool.getconn()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM events WHERE id = %(id)s",
                       {'id': event_id})
        result = cursor.fetchone()

        cursor.close()
        self.__connection_pool.putconn(connection)

        return result


Result.register(PostgresResult)
Backend.register(PostgresBackend)
