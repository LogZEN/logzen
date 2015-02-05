from hamcrest import *

from logzen.db import session
from test_db import DatabaseTestCase
from util import *


class LogsTestCase(DatabaseTestCase):
    users = require('logzen.db.users:Users')
    streams = require('logzen.db.streams:Streams')

    logs = require('logzen.logs:Logs')


    def setUp(self):
        mockElasticsearch.start()

        super().setUp()


    def tearDown(self):
        super().tearDown()

        mockElasticsearch.stop()


    def testQueryWithQuerySucceeds(self):
        result = self.logs.queryWithFilter(filter=None,
                                           query={'q': 'a'})

        assert_that(result, is_({'query': {'q': 'a'}}))


    def testQueryWithoutQuerySucceeds(self):
        result = self.logs.queryWithFilter(filter=None)

        assert_that(result, is_({'query': {'match_all': {}}}))


    def testQueryWithFullUserSucceeds(self):
        with session():
            user = self.users.createUser(username='user',
                                         password='user')

        result = self.logs.queryWithUser(user=user,
                                         query={'q': 'a'})

        assert_that(result, is_({'query': {'q': 'a'}}))


    def testQueryWithEmptyUserSucceeds(self):
        with session():
            user = self.users.createUser(username='user',
                                         password='user')

        result = self.logs.queryWithUser(user=user,
                                         query={'q': 'a'})

        assert_that(result, is_({'query': {'q': 'a'}}))


    def testQueryWithRestrictedUserSucceeds(self):
        with session():
            user = self.users.createUser(username='user',
                                         password='user',
                                         filter={'term': {'host': 'localhost'}})

        result = self.logs.queryWithUser(user=user,
                                         query={'q': 'a'})

        assert_that(result, is_({'filter': {'term': {'host': 'localhost'}},
                                 'query': {'q': 'a'}}))


    def testQueryWithFullUserAndFullStreamSucceeds(self):
        with session():
            user = self.users.createUser(username='user',
                                         password='user')

            stream = self.streams.createStream(user=user,
                                               name='stream')

        result = self.logs.queryWithStream(stream=stream,
                                           query={'q': 'a'})

        assert_that(result, is_({'query': {'q': 'a'}}))


    def testQueryWithEmptyUserAndFullStreamSucceeds(self):
        with session():
            user = self.users.createUser(username='user',
                                         password='user')

            stream = self.streams.createStream(user=user,
                                               name='stream')

        result = self.logs.queryWithStream(stream=stream,
                                           query={'q': 'a'})

        assert_that(result, is_({'query': {'q': 'a'}}))


    def testQueryWithRestrictedUserAndFullStreamSucceeds(self):
        with session():
            user = self.users.createUser(username='user',
                                         password='user',
                                         filter={'term': {'host': 'localhost'}})

            stream = self.streams.createStream(user=user,
                                               name='stream')

        result = self.logs.queryWithStream(stream=stream,
                                           query={'q': 'a'})

        assert_that(result, is_({'filter': {'term': {'host': 'localhost'}},
                                 'query': {'q': 'a'}}))


    def testQueryWithFullUserAndEmptyStreamSucceeds(self):
        with session():
            user = self.users.createUser(username='user',
                                         password='user')

            stream = self.streams.createStream(user=user,
                                               name='stream',
                                               filter={})

        result = self.logs.queryWithStream(stream=stream,
                                           query={'q': 'a'})

        assert_that(result, is_({'query': {'q': 'a'}}))


    def testQueryWithEmptyUserAndEmptyStreamSucceeds(self):
        with session():
            user = self.users.createUser(username='user',
                                         password='user')

            stream = self.streams.createStream(user=user,
                                               name='stream',
                                               filter={})

        result = self.logs.queryWithStream(stream=stream,
                                           query={'q': 'a'})

        assert_that(result, is_({'query': {'q': 'a'}}))


    def testQueryWithRestrictedUserAndEmptyStreamSucceeds(self):
        with session():
            user = self.users.createUser(username='user',
                                         password='user',
                                         filter={'term': {'host': 'localhost'}})

            stream = self.streams.createStream(user=user,
                                               name='stream',
                                               filter={})

        result = self.logs.queryWithStream(stream=stream,
                                           query={'q': 'a'})

        assert_that(result, is_({'filter': {'term': {'host': 'localhost'}},
                                 'query': {'q': 'a'}}))


    def testQueryWithFullUserAndRestrictedStreamSucceeds(self):
        with session():
            user = self.users.createUser(username='user',
                                         password='user')

            stream = self.streams.createStream(user=user,
                                               name='stream',
                                               filter={'term': {'severity': 'fatal'}})

        result = self.logs.queryWithStream(stream=stream,
                                           query={'q': 'a'})

        assert_that(result, is_({'filter': {'term': {'severity': 'fatal'}},
                                 'query': {'q': 'a'}}))


    def testQueryWithEmptyUserAndRestrictedStreamSucceeds(self):
        with session():
            user = self.users.createUser(username='user',
                                         password='user')

            stream = self.streams.createStream(user=user,
                                               name='stream',
                                               filter={'term': {'severity': 'fatal'}})

        result = self.logs.queryWithStream(stream=stream,
                                           query={'q': 'a'})

        assert_that(result, is_({'filter': {'term': {'severity': 'fatal'}},
                                 'query': {'q': 'a'}}))


    def testQueryWithRestrictedUserAndRestrictedStreamSucceeds(self):
        with session():
            user = self.users.createUser(username='user',
                                         password='user',
                                         filter={'term': {'host': 'localhost'}})

            stream = self.streams.createStream(user=user,
                                               name='stream',
                                               filter={'term': {'severity': 'fatal'}})

        result = self.logs.queryWithStream(stream=stream,
                                           query={'q': 'a'})

        assert_that(result, is_({'filter': {'and': [{'term': {'host': 'localhost'}},
                                                    {'term': {'severity': 'fatal'}}]},
                                 'query': {'q': 'a'}}))

