#!python
# encoding: utf-8

# Created by djg-m at 07.01.2021

from handling_db import SqlHandling


class ManageDB:
    """
    Creates a database and relations for messenger application.
    """
    def __init__(self, db):
        self.database = db
        self.db = None

    def create_db(self):
        """
        Creates a database.
        :return: None
        :rtype: None
        """
        self.db = SqlHandling()
        self.db.do_database(self.database)

    def create_users_table(self):
        """
        Creates user relation.
        :return: None
        :rtype: None
        """
        sql = ("CREATE TABLE users ("
               "id serial PRIMARY KEY,"
               "username VARCHAR(255),"
               "hashed_password BYTEA"
               ")")
        self.db.do_query(sql)

    def create_messages_table(self):
        """
        Creates messages relation.
        :return: None
        :rtype: None
        """
        sql = ("CREATE TABLE messages ("
               "id serial PRIMARY KEY,"
               "from_id INT REFERENCES users(id),"
               "to_id INT REFERENCES users(id),"
               "message TEXT,"
               "creation_date TIMESTAMP DEFAULT current_timestamp"
               ")")
        self.db.do_query(sql)


if __name__ == "__main__":
    db = ManageDB('msg_t01')
    db.create_db()
    db.create_users_table()
    db.create_messages_table()
