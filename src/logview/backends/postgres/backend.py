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

from logview.config import Config
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
              AND reported_time >= COALESCE(%(start_time)s, reported_time)
              AND reported_time <= COALESCE(%(end_time)s, reported_time)
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


class PostgresBackend(Backend):
    def __init__(self):
        self.__connection_pool = psycopg2.pool.ThreadedConnectionPool(minconn = int(Config().logview['backend.minconn']),
                                                                      maxconn = int(Config().logview['backend.maxconn']),
                                                                      host = Config().logview['backend.server'],
                                                                      port = int(Config().logview['backend.port']),
                                                                      database = Config().logview['backend.database'],
                                                                      user = Config().logview['backend.username'],
                                                                      password = Config().logview['backend.password'],
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

    def event_peaks(self,
                    time):
        connection = self.__connection_pool.getconn()
        cursor = connection.cursor()

        cursor.execute('''
            SELECT host, COUNT(*) AS count
            FROM events
            WHERE reported_time > %(time)s
            GROUP BY host
            ORDER BY count DESC
            LIMIT 5;
        ''', {"time": time})

        result = cursor.fetchall()

        cursor.close()
        self.__connection_pool.putconn(connection)

        return result

    def event_count_by_host(self):
        connection = self.__connection_pool.getconn()
        cursor = connection.cursor()

        cursor.execute('''
            SELECT host, COUNT(*) AS count
            FROM events
            GROUP BY host
            ORDER BY count DESC;
        ''')

        result = cursor.fetchall()

        cursor.close()
        self.__connection_pool.putconn(connection)

        return result

    def event_count_by_time(self,
                            filters,
                            steps):
        connection = self.__connection_pool.getconn()
        cursor = connection.cursor()

        sql = ('''
            SELECT
                series.timestamp AS time,
                COUNT(event.timestamp) AS count
            FROM generate_series(date_trunc(%(steps)s, %(start_time)s),
                                 date_trunc(%(steps)s, %(end_time)s),
                                 ('1 ' || %(steps)s)::interval) AS series(timestamp)
            LEFT OUTER JOIN (
                SELECT
                    date_trunc(%(steps)s, reported_time) AS timestamp
                FROM events
                WHERE host LIKE COALESCE(%(host)s, host)
                  AND facility LIKE COALESCE(%(facility)s, facility)
                  AND severity LIKE COALESCE(%(severity)s, severity)
                  AND program LIKE COALESCE(%(program)s, program)
                  AND message LIKE COALESCE(%(message)s, message)
                  AND reported_time >= %(start_time)s
                  AND reported_time <= %(end_time)s) AS event
              ON (series.timestamp = event.timestamp)
            GROUP BY series.timestamp
            ORDER BY series.timestamp;
        ''')

        parameters = collections.defaultdict(lambda: None, filters)
        parameters['steps'] = steps

        cursor.execute(sql, parameters)
        result = cursor.fetchall()

        cursor.close()
        self.__connection_pool.putconn(connection)

        return result

    def event_timestamp_range(self):
        connection = self.__connection_pool.getconn()
        cursor = connection.cursor()

        sql = ('''
            SELECT min(reported_time) AS min, max(reported_time) AS max
            FROM events;
        ''')

        cursor.execute(sql)
        result = cursor.fetchone()

        cursor.close()
        self.__connection_pool.putconn(connection)

        return result['min'], result['max']

    def new_events(self,
                   filter):
        connection = self.__connection_pool.getconn()
        cursor = connection.cursor()

        where = ""
        if filter != 7:
            if filter >= 1:
                where += "WHERE severity = 'alert'"
            if filter >= 2:
                where += " OR severity = 'crit'"
            if filter >= 3:
                where += " OR severity = 'err'"
            if filter >= 4:
                where += " OR severity = 'warning'"
            if filter >= 5:
                where += " OR severity = 'notice'"
            if filter >= 6:
                where += " OR severity = 'info'"

        sql = '''
            SELECT reported_time, host, severity, message
            FROM events
        ''' + where + '''
            ORDER BY reported_time DESC
            LIMIT 15;
        '''

        cursor.execute(sql)
        result = cursor.fetchall()

        cursor.close()
        self.__connection_pool.putconn(connection)

        return result

    def get_severity_count(self,
                           host):
        connection = self.__connection_pool.getconn()
        cursor = connection.cursor()

        sql = '''
            SELECT severity, COUNT(*) as count
            FROM events
            WHERE host LIKE COALESCE(%(host)s, host)
            GROUP BY severity
            ORDER BY count DESC;
        '''
        cursor.execute(sql, collections.defaultdict(lambda: None, {'host': host}))
        result = cursor.fetchall()

        cursor.close()
        self.__connection_pool.putconn(connection)

        return result


    def get_hosts(self):
        connection = self.__connection_pool.getconn()
        cursor = connection.cursor()

        cursor.execute('SELECT host FROM events GROUP BY host;')
        result = cursor.fetchall()

        cursor.close()
        self.__connection_pool.putconn(connection)

        return result

Result.register(PostgresResult)
Backend.register(PostgresBackend)
