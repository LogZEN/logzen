import json

from hamcrest import *

from require import *
from require.mock import *

from logzen.db import session

from test_api import ApiTestCase

from util import *



class UserApiTestCase(ApiTestCase):
    users = require('logzen.db.users:Users')


    def setUp(self):
        super().setUp()

        with session():
            self.user = self.users.createUser(username='user',
                                              password='user')


    def testAuthenticatedAccessSucceeds(self):
        self.client.post('/api/v1/token',
                         data=json.dumps({'username': 'user',
                                          'password': 'user'}))

        resp = self.client.get('/api/v1/user')

        assert_that(resp.status_code, is_(200))


    def testAnonymousAccessFails(self):
        resp = self.client.get('/api/v1/user')

        assert_that(resp.status_code, is_(401))
        assert_that(resp.data, is_(b'Authentication required'))


class UserAccountApiTestCase(ApiTestCase):
    users = require('logzen.db.users:Users')


    def setUp(self):
        super().setUp()

        with session():
            self.user = self.users.createUser(username='user',
                                              password='user')

        self.client.post('/api/v1/token',
                         data=json.dumps({'username': 'user',
                                          'password': 'user'}))


    def testFetchingAccountInfoSucceeds(self):
        resp = self.client.get('/api/v1/user/account')

        assert_that(resp.status_code, is_(200))
        assert_that(json.loads(resp.data.decode('utf8')), is_({'username': 'user'}))


class UserStreamsApiTestCase(ApiTestCase):
    users = require('logzen.db.users:Users')
    streams = require('logzen.db.streams:Streams')


    def setUp(self):
        super().setUp()

        with session():
            self.user = self.users.createUser(username='user',
                                              password='user')

        self.client.post('/api/v1/token',
                         data=json.dumps({'username': 'user',
                                          'password': 'user'}))


    def testCreatingStreamSucceeds(self):
        resp = self.client.post('/api/v1/user/streams',
                                data=json.dumps({'name': 'test',
                                                 'description': 'For testing purposes only',
                                                 'filter': {'foo': 42,
                                                            'bar': 23}}))

        assert_that(resp.status_code, is_(200))

        with session():
            user = self.users.getUserByName('user')

            assert_that(user.streams, has_length(1))
            assert_that(user.streams, has_items('test'))


    def testDeletingStreamSucceeds(self):
        with session():
            self.streams.createStream(user=self.user,
                                      name='test',
                                      filter={})

        resp = self.client.delete('/api/v1/user/streams/test')

        assert_that(resp.status_code, is_(200))

        with session():
            user = self.users.getUserByName('user')

            assert_that(user.streams, is_(empty()))


    def testListingStreamsSucceeds(self):
        with session():
            self.streams.createStream(user=self.user,
                                      name='test1',
                                      filter={})
            self.streams.createStream(user=self.user,
                                      name='test2',
                                      filter={})
            self.streams.createStream(user=self.user,
                                      name='test3',
                                      filter={})

        resp = self.client.get('/api/v1/user/streams')

        assert_that(resp.status_code, is_(200))
        assert_that(json.loads(resp.data.decode('utf8')), is_({'test1': {'description': '',
                                                                         'filter': {}},
                                                               'test2': {'description': '',
                                                                         'filter': {}},
                                                               'test3': {'description': '',
                                                                         'filter': {}}}))


    def testFetchingStreamSucceeds(self):
        with session():
            self.streams.createStream(user=self.user,
                                      name='test',
                                      filter={})

        resp = self.client.get('/api/v1/user/streams/test')

        assert_that(resp.status_code, is_(200))
        assert_that(json.loads(resp.data.decode('utf8')), is_({'name': 'test',
                                                               'description': '',
                                                               'filter': {}}))


    def testUpdatingStreamSucceeds(self):
        with session():
            self.streams.createStream(user=self.user,
                                      name='test',
                                      filter={})

        resp = self.client.put('/api/v1/user/streams/test',
                               data=json.dumps({'name': 'toast',
                                                'description': 'x',
                                                'filter': {'foo': 'bar'}}))

        assert_that(resp.status_code, is_(200))

        with session():
            user = self.users.getUserByName('user')
            stream = user.streams['toast']

            assert_that(stream.name, is_('toast'))
            assert_that(stream.description, is_('x'))
            assert_that(stream.filter, is_({'foo': 'bar'}))


class UserLogsApiTestCase(ApiTestCase):
    users = require('logzen.db.users:Users')
    streams = require('logzen.db.streams:Streams')


    def setUp(self):
        mockElasticsearch.start()

        super().setUp()

        with session():
            self.user = self.users.createUser(username='user',
                                              password='user')

            self.stream = self.streams.createStream(self.user,
                                                    name='foo',
                                                    filter={})

        self.client.post('/api/v1/token',
                         data=json.dumps({'username': 'user',
                                          'password': 'user'}))

    def tearDown(self):
        super().tearDown()

        mockElasticsearch.stop()


    def testFetchWithMatchAllSucceeds(self):
        resp = self.client.post('/api/v1/user/logs/*',
                                data=json.dumps(None))

        assert_that(resp.status_code, is_(200))
        assert_that(json.loads(resp.data.decode('utf8')),
                    is_({'query': {'match_all': {}}}))


    def testFetchWithStreamSucceeds(self):
        resp = self.client.post('/api/v1/user/logs/foo',
                                data=json.dumps(None))

        assert_that(resp.status_code, is_(200))
        assert_that(json.loads(resp.data.decode('utf8')),
                    is_({'query': {'match_all': {}}}))


    def testFetchWithUnknownStreamFails(self):
        resp = self.client.post('/api/v1/user/logs/unknown',
                                data=json.dumps(None))

        assert_that(resp.status_code, is_(404))
