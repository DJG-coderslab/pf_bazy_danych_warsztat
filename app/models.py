#!python
# encoding: utf-8

# Created by djg-m at 07.01.2021

import bcrypt
import string

from random import choice

from handling_db import SqlHandling


class Messenger:
    """
    Parent class for class User, Users and Message
    """

    DATABASE = 'msg_t01'
    DB = SqlHandling(DATABASE)

    def __init__(self):
        self.insert_dict = None
        self._id = -1
        self._database = 'msg_t01'
        self._db = SqlHandling(self._database)

    @property
    def id(self):
        """
        Returns users id in database
        :return: users id
        :rtype: int
        """
        return self._id

    def _tuple_to_object(self, data_in_tuple, obj=None):
        """
        Creates a new object from namedtuple

        :param data_in_tuple: namedtuple where name is a name of columns
                              from DB
        :type data_in_tuple: namedtuple
        :return: True
        :rtype: bool
        """
        new_obj = obj() if obj else self
        for i, name in enumerate(data_in_tuple._fields):
            if name == 'id':
                name = '_id'
            new_obj.__dict__[name] = data_in_tuple[i]
        return new_obj


class Password:
    """
    Class for managing passwords

    Here you can set up the password for user after reading from DB or
    handling passed password as string. Class can hashed the password,
    setting up and checking constraints and compare hashed password with
    passed string.
    """
    def __init__(self, password=None):
        self._hashed_passwd = None
        self._min_length = 8
        if password:
            self.hash = password

    @property
    def hash(self):
        """
        Returned password is as bytes object
        :return: hashed password
        :rtype: bytes
        """
        return self._hashed_passwd

    @hash.setter
    def hash(self, passwd):
        """
        Setting password for object argument _hashed.password

        If param is type of bytes it is only assigned to the argument else
        is called the _hash_password method

        :param passwd: hashed or plain text password
        :type passwd: bytes or str
        :return: None
        :rtype: None
        """
        # TODO this methot sould only set up the hashed password or
        #  should be removed
        if isinstance(passwd, bytes):
            self._hashed_passwd = passwd
        else:
            self.check_constraints(passwd)
            self._hashed_passwd = self._hash_password(passwd)

    def check_constraints(self, param):
        """
        Checks the password for restrictions.

        :param param: password
        :type param: str
        :return: True if password is correct
        :rtype: None
        """
        if len(param) < self._min_length:
            raise ValueError(f"The length of password need to be more "
                             f"than {self._min_length}")
        return True

    @staticmethod
    def _hash_password(passwd):
        """
        Hashing the password.

        :param passwd: users password
        :type passwd:str
        :return: hashed password
        :rtype: bytes
        """
        return bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt(14))

    def compare_hash_password(self, passwd):
        """
        Check the correctness of the password

        :param passwd: password for checking
        :type passwd: str
        :return: None
        :rtype: None or True
        """
        if not bcrypt.checkpw(passwd.encode('utf-8'), self.hash):
            raise ValueError("Bad password...")
        return True

    def generate_password(self, length=17):
        """
        Generating a random password.

        :param length: default length of password (not minimal)
        :type length: int
        :return: random string as password
        :rtype: str
        """
        alphabet = (string.ascii_uppercase + string.ascii_lowercase
                    + string.digits + string.punctuation)
        length = length if length > self._min_length else self._min_length
        password = ""
        for i in range(length):
            password += choice(alphabet)
        # TODO to think does that make sense?
        return password


class User(Messenger):
    """
    Manage an user.
    """

    TABLE = 'users'

    def __init__(self, username=None, password=None, **kwargs):
        super().__init__()
        self.username = None
        self.passwd = Password()
        self._hashed_password = None
        self._is_authorize = False
        if username and password:
            self.new_user(username=username, passwd=password)

    @property
    def password(self):
        """
        Returns nothing, True
        :return: True
        :rtype: bool
        """
        return True

    @password.setter
    def password(self, passwd):
        self.passwd.hash = passwd
        # TODO here there isn't writing to DB a new password!

    @property
    def is_authorized(self):
        """
        Returns state of user's authorisation

        :return:
        :rtype: bool
        """
        # TODO to think, does the user should be authorized?
        return self._is_authorize

    def authorize(self, password):
        """
        can set up the authorized switch for user after passed good password

        :param password: plain text password
        :type password: str
        :return: True or False
        :rtype: bool
        """
        try:
            self.passwd.compare_hash_password(password)
        except ValueError as err:
            self._is_authorize = False
            return False
        else:
            self._is_authorize = True
            return True

    def new_user(self, username=None, passwd=None):
        """
        creates a new User object based on username and password
        :param username: name of new user
        :type username: str
        :param passwd: password as plain text
        :type passwd: str
        :return: True or False
        :rtype: bool
        """
        try:
            self.passwd = Password(passwd)
            # TODO self.password = passwd
        except ValueError as err:
            print(err)
            # TODO I don't know if it the best way to end method
            #  mayby better will be here omit this exception?
            return None
        data_to_save = {'username': username,
                        'hashed_password': self.passwd.hash}
        result = self._db.insert_data(self.TABLE, data_to_save)
        if not result:
            raise ValueError("Coś się nie udało")
        # TODO needed to detail the error
        self._tuple_to_object(result[0])
        self.password = bytes(result[0].hashed_password)
        return True

    def _from_db(self, column=None, condition=None):
        """
        Database query for user by different column

        :param column: column name for database query
        :type column: str
        :param condition: condition for query
        :type condition: str or int
        :return: list of namedtuple with data from database
        :rtype: list
        """
        where = f" WHERE {column} = %s" if condition else ""
        sql = (f"SELECT id, username, hashed_password FROM "
               f"{self.TABLE} {where}")
        params = [condition]
        result = self._db.do_query(sql, params)
        if not result:
            raise ValueError("Brak szukanego użytkownika")
        return result

    def load_by_id(self, id_):
        """
        loads the data to the object from DB according to id

        :param id_:  number id in DB
        :type id_:  int
        :return:  True or False
        :rtype: bool
        """
        result = self._from_db(column='id', condition=id_)[0]
        self._tuple_to_object(result)
        self.password = bytes(result.hashed_password)
        return True

    def load_by_username(self, username):
        """
        loads the data to the object from DB according to username

        :param username: name of user
        :type username: str
        :return: True or False
        :rtype:bool
        """
        result = self._from_db(column='username', condition=username)[0]
        self._tuple_to_object(result)
        self.password = bytes(result.hashed_password)
        return True

    def load_all_users(self):
        """
        Returns abject Message for all messages to receiver

        :return: generator of object User
        :rtype: user
        """
        result = self._from_db()
        return (self._tuple_to_object(user, User) for user in result)

    def delete_user(self):
        """
        Deletes current user
        :return: None
        :rtype: None
        """
        if not self.is_authorized:
            raise ValueError("Nie można usunąć nie zalogowanego uzytkownika")
        sql = f"DELETE FROM {self.TABLE} WHERE id = %s"
        params = [self._id]
        if self._db.do_query(sql, params):
            self._id = -1

    """ Classmethod as a factory """

    @classmethod
    def all_users(cls):
        users = User()
        return users.load_all_users()


class Message(Messenger):
    """
    Manages messages
    """

    TABLE = 'messages'

    def __init__(self, **kwargs):
        """
        Returns a new Message instance

        Arguments:

        new_message - tuple or list: (id_sender, id_receiver, message)

        :param kwargs: dictionary with parameters
        :type kwargs: dict
        """
        super().__init__()
        self.from_id = None
        self.to_id = None
        self.message = None
        self.creation_data = None
        self._options = 'new_message'.split()
        for option in self._options:
            if option in kwargs:
                self._do_action(option, kwargs[option])
                break

    def _do_action(self, option, val):
        if option == 'new_message':
            self.new_message(*val)

    def new_message(self, from_id, to_id, msg):
        """
        Creates a new object Message

        :param from_id: id sender user
        :type from_id: int
        :param to_id: id receiver user
        :type to_id: int
        :param msg: message
        :type msg: str
        :return: a new object Message
        :rtype: Message
        """
        data_to_save = {'from_id': from_id, 'to_id': to_id, 'message': msg}
        result = self._db.insert_data(self.TABLE, data_to_save)
        if not result:
            raise ValueError("Nie udało się zapisać wiadomości")
        self._tuple_to_object(result[0])

    def _load_from_db(self, column=None, condition=None):
        """
        Database query for message by different column

        :param column: column name for database query
        :type column: str
        :param condition: condition for query
        :type condition: str or int
        :return: list of namedtuple with data from database
        :rtype: list
        """
        where = f" WHERE {column} = %s" if condition else ""
        sql = (f"SELECT from_id, to_id, message, creation_date FROM "
               f"{self.TABLE} {where}")
        params = [condition]
        result = self._db.do_query(sql, params)
        if not result:
            raise ValueError("Brak szukanych wiadomości")
        return result

    def load_all_messages(self):
        """
        Returns a generator with all messages as namedtuple

        :return: generator of namedtuple where name is a name of column from DB
        :rtype: namedtuple
        """
        result = self._load_from_db()
        return (self._tuple_to_object(msg, Message) for msg in result)

    def load_by_sender(self, user_id):
        """
        Returns abject Message for all messages to sender

        :param user_id: id sender from table users
        :type user_id: int
        :return: generator of object Message
        :rtype: Message
        """
        result = self._load_from_db(column='from_id', condition=user_id)
        return (self._tuple_to_object(msg, Message) for msg in result)

    def load_by_receiver(self, user_id):
        """
        Returns abject Message for all messages to receiver

        :param user_id: id receiver from table users
        :type user_id: int
        :return: generator of object Message
        :rtype: Message
        """
        result = self._load_from_db(column='to_id', condition=user_id)
        return (self._tuple_to_object(msg, Message) for msg in result)

    def load_by_id(self):
        pass

    """ Classmethod as a factory """

    @classmethod
    def all_messages(cls):
        """
        Returns all messages as generator of Message objects

        :return: generator of Message object
        :rtype: Message
        """
        msg = Message()
        return msg.load_all_messages()
