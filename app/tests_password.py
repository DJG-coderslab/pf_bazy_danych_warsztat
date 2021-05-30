#!python
# encoding: utf-8

# Created by Preload at 2021-01-12

import unittest

from models import Password


class TestPassword(unittest.TestCase):

    def test_new_password(self):
        self.assertTrue(Password())
        self.assertTrue(Password('xxxxxxxxx'))
        passwd = Password('xxxxxxxxx')
        self.assertEqual(passwd.hash[:7], b'$2b$14$')
        with self.assertRaises(ValueError):
            Password("xxx")

    def test_check_constraints(self):
        passwd = Password()
        with self.assertRaises(ValueError):
            passwd.check_constraints('xxx')

    def test_compare_passwords(self):
        password = Password('xxxxxxxxx')
        self.assertTrue(password.compare_hash_password('xxxxxxxxx'))
        with self.assertRaises(ValueError):
            password.compare_hash_password('yyyyyyyyy')


if __name__ == "__main__":
    unittest.main(verbosity=2)
