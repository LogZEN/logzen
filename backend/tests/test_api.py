import unittest

from hamcrest import *

import werkzeug.test
import werkzeug.wrappers

import json

from require import *

from logzen.db import session



@export(engine='logzen.db:Engine')
def TestConnection(engine):
    return engine.connect()



@extend('logzen.db:SessionFactory',
        connection='test_api:TestConnection')
def TestSessionFactory(factory,
                       connection):
    factory.configure(bind=connection)



class ApiTestCase(unittest.TestCase):
    testConnection = require('test_api:TestConnection')

    app = require('logzen.web:App')

    session = require('logzen.db:Session')


    def setUp(self):
        # Begin a manual transaction
        self.transaction = self.testConnection.begin()

        # Create the request client
        self.client = werkzeug.test.Client(self.app,
                                           response_wrapper=werkzeug.wrappers.BaseResponse,
                                           use_cookies=True)


    def tearDown(self):
        # Destroy the request client
        del self.client

        self.session.rollback()
        self.session.close()

        # Rollback all changes
        self.transaction.rollback()



class AuthenticationApiTestCase(ApiTestCase):
    users = require('logzen.db.users:Users')


    def setUp(self):
        super(AuthenticationApiTestCase, self).setUp()

        with session():
            self.user = self.users.createUser(username='admin',
                                              password='admin')


    def testAuthenticationSucceeds(self):
        resp = self.client.post('/api/v1/token',
                                data=json.dumps({'username': 'admin',
                                                 'password': 'admin'}))

        assert_that(resp.status_code, is_(200))
        assert_that(resp.data, is_(empty()))


    def testAuthenticationWithInsufficientDataFails(self):
        resp = self.client.post('/api/v1/token',
                                data=json.dumps({'foo': 'bar'}))

        assert_that(resp.status_code, is_(400))
        assert_that(resp.data, is_(b'Malformed data'))


    def testAuthenticationWithWrongPasswordFails(self):
        resp = self.client.post('/api/v1/token',
                                data=json.dumps({'username': 'admin',
                                                 'password': 'WRONG'}))

        assert_that(resp.status_code, is_(401))
        assert_that(resp.data, is_(b'Wrong username or password'))


class UserApiTestCase(ApiTestCase):
    users = require('logzen.db.users:Users')


    def setUp(self):
        super(UserApiTestCase, self).setUp()

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
        super(UserAccountApiTestCase, self).setUp()

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


class AdminApiTestCase(ApiTestCase):
    users = require('logzen.db.users:Users')


    def setUp(self):
        super(AdminApiTestCase, self).setUp()

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
        super(AdminUsersApiTestCase, self).setUp()

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

        user = self.users.getUser('marvin')

        assert_that(user, is_(not_none()))
        assert_that(user, has_properties(username='marvin',
                                         admin=True))
