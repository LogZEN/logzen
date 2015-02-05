import json

from hamcrest import *

from require import *
from logzen.db import session

from test_api import ApiTestCase


class AdminApiTestCase(ApiTestCase):
    users = require('logzen.db.users:Users')


    def setUp(self):
        super().setUp()

        with session():
            self.user = self.users.createUser(username='user',
                                              password='user')

            self.admin = self.users.createUser(username='admin',
                                               password='admin',
                                               admin=True)


    def testAuthorizedAccessSucceeds(self):
        self.client.post('/api/v1/token',
                         data=json.dumps({'username': 'admin',
                                          'password': 'admin'}))

        resp = self.client.get('/api/v1/admin/users')

        assert_that(resp.status_code, is_(200))


    def testAuthenticatedNotAuthorizedAccessFails(self):
        self.client.post('/api/v1/token',
                         data=json.dumps({'username': 'user',
                                          'password': 'user'}))

        resp = self.client.get('/api/v1/admin/users')

        assert_that(resp.status_code, is_(401))
        assert_that(resp.data, is_(b'Authentication required'))


    def testAnonymousAccessFails(self):
        resp = self.client.get('/api/v1/admin/users')

        assert_that(resp.status_code, is_(401))
        assert_that(resp.data, is_(b'Authentication required'))


class AdminUsersApiTestCase(ApiTestCase):
    users = require('logzen.db.users:Users')


    def setUp(self):
        super().setUp()

        with session():
            self.admin = self.users.createUser(username='admin',
                                               password='admin',
                                               admin=True)

            self.user1 = self.users.createUser(username='user1',
                                               password='test')
            self.user2 = self.users.createUser(username='user2',
                                               password='test')
            self.user3 = self.users.createUser(username='user3',
                                               password='test')

        self.client.post('/api/v1/token',
                         data=json.dumps({'username': 'admin',
                                          'password': 'admin'}))


    def testFetchingUserListSucceeds(self):
        resp = self.client.get('/api/v1/admin/users')

        assert_that(resp.status_code, is_(200))
        assert_that(json.loads(resp.data.decode('utf8')), is_({'admin': {'username': 'admin',
                                                                         'admin': True},
                                                               'user1': {'username': 'user1',
                                                                         'admin': False},
                                                               'user2': {'username': 'user2',
                                                                         'admin': False},
                                                               'user3': {'username': 'user3',
                                                                         'admin': False}}))


    def testCreatingUserSucceeds(self):
        resp = self.client.post('/api/v1/admin/users',
                                data=json.dumps({'username': 'marvin',
                                                 'password': 'test123',
                                                 'admin': True}))

        assert_that(resp.status_code, is_(200))
        assert_that(resp.data, is_(b''))

        user = self.users.getUserByName('marvin')

        assert_that(user, is_(not_none()))
        assert_that(user, has_properties(username='marvin',
                                         admin=True))
