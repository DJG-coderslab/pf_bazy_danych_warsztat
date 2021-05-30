#!python
# encoding: utf-8

# Created by Preload at 2021-01-13


import unittest

from models import Password, User


class TestMsg(unittest.TestCase):

    def test_user_for_test(self):
        user = User()
        self.assertFalse(user._is_authorize)


if __name__ == "__main__":
    unittest.main(verbosity=2)
