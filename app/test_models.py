#!python
# encoding: utf-8

# Created by Preload at 2021-01-12


from create_db import ManageDB
from handling_db import SqlHandling


class Env:
    def __init__(self):
        self.database = 'test_msg'
        self.db = SqlHandling(self.database)
        self.env = ManageDB(self.database)
        self.end = 'END'

    def do_db(self):
        self.env.create_db()
        self.env.create_users_table()
        self.env.create_messages_table()
