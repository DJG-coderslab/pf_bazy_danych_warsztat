#!python
# encoding: utf-8

# Created by Preload at 2021-01-12

import unittest

from models import Password, User
from test_models import Env


class TestUser(unittest.TestCase, Env):

    ENV = Env()

    def __init__(self, *args, **kwargs):
        super(TestUser, self).__init__(*args, **kwargs)
        Env.__init__(self)
        # self.do_db()
        self.end = "END"

    #
    # def test_create_user(self):
    #     self.assertTrue(User())
    #     user = User()
    #     self.assertIsNone(user.username)
    #     # self.assertIsNone(user._hashed_password)
    #     self.assertFalse(user._authorized_user)
    #     self.assertIsInstance(user.passwd, Password)
    #
    # def test_user_by_id(self):
    #     self.db.insert_data('users', {'username': 'Ula',
    #                                   'hashed_password': 'UlaPassword'})
    #     user = User()
    #     self.assertTrue(user.load_by_id(1))
    #     self.assertEqual(user._id, 1)
    #     self.assertTrue(user.username, 'Ula')
    #     # self.assertTrue(user._hashed_password, b'UlaPassword')
    #
    # def test_user_by_username(self):
    #     self.db.insert_data('users', {'username': 'Ala',
    #                                   'hashed_password': 'AlaPassword'})
    #     user = User()
    #     self.assertTrue(user.load_by_id(2))
    #     self.assertEqual(user._id, 2)
    #     self.assertTrue(user.username, 'Ala')
    #     # self.assertTrue(user._hashed_password, b'AlaPassword')
    #
    # def test_return_password(self):
    #     # TODO does this test make a sense?
    #     self.db.insert_data('users', {'username': 'Ela',
    #                                   'hashed_password': 'ElaPassword'})
    #     user = User()
    #     user.load_by_username('Ela')
    #     self.assertEqual(user.password[:7], b'$2b$14$')
    #
    # def test_check_password(self):
    #     self.db.insert_data('users', {'username': 'Ula',
    #                                   'hashed_password': 'UlaPassword'})
    #     user = User()
    #     user.load_by_username('Ula')
    #     user.password = 'UlaPassword'
    #     self.assertTrue(user.passwd.compare_hash_password('UlaPassword'))
    #     self.assertEqual(user.passwd.hash[:7], b'$2b$14$')
    #
    # def test_new_u(self):
    #     user = User(username='Ana', password='AnaPassword')
    #     self.assertIsInstance(user, User)
    #     self.assertEqual(user.username, 'Ana')
    #     self.assertEqual(user.password[:7], b'$2b$14$')
    #
    """
    user = User(load_by_id = id)
    user = User(load_by_name = username)
    user.delete_user(id)
    user.load_by_id(id)
    user.load_by_name(username)
    """
    #
    # @classmethod
    # def setUpClass(cls) -> None:
    #     cls.ENV.do_db()
    #
    # @classmethod
    # def tearDownClass(cls):
    #     sql = f"DROP TABLE users CASCADE"
    #     cls.ENV.db.do_query(sql)
    #


class UserTest(unittest.TestCase, Env):

    ENV = Env()

    def __init__(self, *args, **kwargs):
        super(UserTest, self).__init__(*args, **kwargs)
        Env.__init__(self)
        # self.do_db()
        self.end = "END"

    @classmethod
    def setUpClass(cls) -> None:
        cls.ENV.do_db()

    @classmethod
    def tearDownClass(cls):
        sql = "DROP TABLE users CASCADE"
        cls.ENV.db.do_query(sql)

    """ Study cases"""

    def test_user_without_parameters(self):
        """
        creating a new object User, without parameters:
        - should occur object class User,
        - this object should has:
            - arg passwd as an object Password with argument password None
            - arg username as None
            - arg _authorized as False
        """
        user = User()
        self.assertIsInstance(user.passwd, Password)
        self.assertIsNone(user.username)
        self.assertFalse(user._is_authorize)

    def test_load_user_by_username(self):
        """
        loading users data from DB by username
        - should occur object class User,
        - this object should has:
            - arg passwd as an object Password with argument password
              as bytes
            - arg username as string
            - arg _authorized as False
        """
        self.db.insert_data('users', {'username': 'Ala',
                                      'hashed_password': 'AlaPassword'})
        user = User()
        user._db = self.db
        user.DB = self.db
        self.assertTrue(user.load_by_username('Ala'))
        self.assertEqual(user._id, 1)
        self.assertTrue(user.username, 'Ala')

    def test_load_user_by_id(self):
        """
        loading users data from DB by id
        - should occur object class User,
        - this object should has:
            - arg passwd as an object Password with argument password
              as bytes
            - arg username as string
            - arg _authorized as False
        """
        user = User()
        self.db.insert_data('users', {'username': 'Ela',
                                      'hashed_password': 'ElaPassword'})
        user = User()
        user._db = self.db
        user.DB = self.db
        self.assertTrue(user.load_by_id(2))
        self.assertEqual(user._id, 2)
        self.assertTrue(user.username, 'Ela')

    def test_change_users_password(self):
        user = User(username='Ola', password='OlaPassword')
        old_passwd = user.password
        user.password = "NewPassword"
        self.assertNotEqual(user.password, old_passwd)

    def test_authorization_user_good_password(self):
        user = User(username='Ula', password='GoodPassword')
        self.assertFalse(user.is_authorized)
        user.is_authorized = 'GoodPassword'
        self.assertTrue(user.is_authorized)

    def test_authorization_user_bad_password(self):
        user = User(username='Ula', password='GoodPassword')
        self.assertFalse(user.is_authorized)
        user.is_authorized = 'BadPassword'
        self.assertFalse(user.is_authorized)
        user.is_authorized = 'GoodPassword'
        self.assertTrue(user.is_authorized)
        user.is_authorized = 'BadPassword'
        self.assertFalse(user.is_authorized)

    def test_deleting_user(self):
        user = 'User_for_del'
        passwd = 'GoodPassword'
        user = User(username=user, password=passwd)

        """
        User z parametrami:
            - user i passwd
            - load_by_id=
            - load_by_name=
        kasowanie usera
        """


if __name__ == "__main__":
    unittest.main(verbosity=2)
