import unittest
import json

from hamcrest import *

import werkzeug.test
import werkzeug.wrappers

from logzen.db import session

from util import *



class ApiTestCase(unittest.TestCase):
    testConnection = require('util:TestConnection')

    app = require('logzen.web:App')

    session = require('logzen.db:Session')


    def setUp(self):
        mockConfigFile.start()

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

        mockConfigFile.stop()


class AuthenticationApiTestCase(ApiTestCase):
    users = require('logzen.db.users:Users')


    def setUp(self):
        super().setUp()

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
