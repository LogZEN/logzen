import unittest

from hamcrest import *

from logzen.db import session
from logzen.db.users import User, Password

from util import *



class DatabaseTestCase(unittest.TestCase):
    testConnection = require('util:TestConnection')

    session = require('logzen.db:Session')


    def setUp(self):
        mockConfigFile.start()

        # Begin a manual transaction
        self.transaction = self.testConnection.begin()



    def tearDown(self):
        self.session.rollback()
        self.session.close()

        # Rollback all changes
        self.transaction.rollback()

        mockConfigFile.stop()



class UserDatabaseTestCase(DatabaseTestCase):

    users = require('logzen.db.users:Users')


    def setUp(self):
        super().setUp()

        with session():
            self.users.createUser(username='test',
                                  password='plain')

    def testPasswordIsHashedAfterCreation(self):
        user = User(username='test',
                    password='plain')

        assert_that(user.password, is_(instance_of(Password)))


    def testPasswordIsHashedAfterFetching(self):
        user = self.users.getUserByName('test')

        assert_that(user.password, is_(instance_of(Password)))


    def testPasswordVerificytionSucceeds(self):
        user = self.users.getUserByName('test')

        assert_that(user.password == 'plain', is_(True))


    def testPasswordVerificytionWithWrongPasswordFails(self):
        user = self.users.getUserByName('test')

        assert_that(user.password == 'WRONG!', is_(False))



