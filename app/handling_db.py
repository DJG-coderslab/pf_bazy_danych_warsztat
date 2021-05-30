#!python
# encoding: utf-8

# Created by djg-m at 16.12.2020

from platform import uname
from prettytable import from_db_cursor
from psycopg2 import connect, OperationalError, ProgrammingError, errors, Error
from psycopg2.extras import NamedTupleCursor


class SqlHandling:
    """
    Class is a wrapper for SQL manipulating

    that was created for less typing repetitive code on lesson work
    """
    if uname().node == "Preload_PC":
        HOST = '10.61.14.35'
    else:
        HOST = '172.17.19.12'
    USER = 'postgres'
    PASSWD = 'coderslab'

    def __init__(self, db=None):
        self.db = db
        self.cnx = None
        self.cursor = None
        self.error = None

    def _execute_sql(self, sql, param=None):
        """
        Connecting to DB and executing an SQL command
        :param sql: SQL command
        :type sql: str
        :return: Status of operation n > 0 n rows was changed, n = 0 any row
                 was changed, n = -1 operation into DB was correct e.g
                 create table
        :rtype: int
        """
        try:
            self.cnx = connect(host=self.HOST, user=self.USER,
                               password=self.PASSWD, database=self.db,
                               cursor_factory=NamedTupleCursor)
            self.cnx.autocommit = True
            self.cursor = self.cnx.cursor()
            self.cursor.execute(sql, param)
            return self.cursor.rowcount
        except OperationalError as err:
            print(f"Połączenie nieudane... {err}")
            self.error = err
        except ProgrammingError as err:
            print(err)
            self.error = err
        except (errors.UniqueViolation, errors.ForeignKeyViolation,
                errors.NotNullViolation) as err:
            print(err)
            self.error = err
        except TypeError as err:
            print(err)
            self.error = err

    def _clean(self):
        """
        Cleaning after connection to DB closing the cursor and the connecting

        :return: None
        :rtype: None
        """
        try:
            self.cursor.close()
        except Exception as err:
            print(err)
            self.error = err
        try:
            self.cnx.close()
        except Exception as err:
            print(err)
            self.error = err

    def do_query(self, sql, param=None):
        """
        Passing an SQL command

        can handling a command that returning something (SELECT)
        and returning nothing (e.g. CREATE TABLE)
        :param param: optional list of values
        :type param: list
        :param sql: SQL command
        :type sql: str
        :return: list of tuple or empty list
        :rtype: list or inr n, 0 , -1
        """
        answer = self._execute_sql(sql, param)
        try:
            answer = self.cursor.fetchall()
        except Error as err:
            pass
            # print(err)
        else:
            self._clean()
        finally:
            return answer

    def insert_data(self, table, dict_data):
        """
        Prepare SQL code for instert data to DB

        :param table:  name of table
        :type table: str
        :param dict_data: dict, where key name is equal as column name
        :type dict_data: dict
        :return:
        :rtype:
        """
        columns = ", ".join(dict_data.keys())
        params = ", ".join(['%s' for _ in dict_data])
        values = list(dict_data.values())
        sql = f"INSERT INTO {table} ({columns}) VALUES ({params}) RETURNING *"
        return self.do_query(sql, values)

    def update(self, table, condition, params):
        """
        Updating a table

        :param table: name of table to update
        :type table: str
        :param condition: name of field for condition and value
        :type condition: tuple (name, value)
        :param params: dict where keys are name of columns, value are value
                       to change
        :type params: dict
        :return: answer from DB 0 no changed int changed number of rows
        :rtype:int
        """
        fields = ", ".join([f"{key} = %s" for key in params.keys()])
        values = list(params.values())
        values.append(condition[1])
        sql = f"UPDATE {table} SET {fields} WHERE {condition[0]} = %s"
        return self.do_query(sql, values)

    def do_database(self, db, delete=False):
        """
        For creating a database

        the existing DB is dropped before creating
        :param db: an SQL command
        :type db: str
        :param delete: delete if exists DB or not
        :type: bool
        :return: None
        :rtype: None
        """
        if delete:
            sql = f"""Drop DATABASE IF EXISTS {db}"""
            self._execute_sql(sql)
        sql = f"""CREATE DATABASE {db}"""
        self._execute_sql(sql)
        self._clean()
        self.db = db

    def print_tab(self, sql):
        """
        Printing the output of SELECT in pretty format

        :param sql: an SQL command SELECT
        :type sql: str
        :return: None
        :rtype: None
        """
        self._execute_sql(sql)
        tab = from_db_cursor(self.cursor)
        print(tab)
        self._clean()


if __name__ == "__main__":
    pass
