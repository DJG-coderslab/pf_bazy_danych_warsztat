#!python
# encoding: utf-8

# Created by djg-m at 08.01.2021

import argparse

from models import User


def users_list():
    """
    Print username of all users

    :return: None
    :rtype: None
    """
    users = User()
    for user in users.load_all_users():
        print(f"{user.username}")


def edit_user(args, user):
    """
    Changes users password
    :param args: CLI parameters in object
    :type args: args
    :param user: user parameter in User object
    :type user: User
    :return: None
    :rtype: None
    """
    # TODO needed to add constraints for e new password
    user.password = args.new_passwd


def del_user(args, user):
    """
    Removes user.
    :param user: users parameters in User object
    :type user: User
    :return: None
    :rtype: None
    """
    user.delete_user()


def new_user(args):
    """
    Creates a new user.
    :param args: CLI parameters in object
    :type args: args
    :return: None
    :rtype: None
    """
    # \TODO missing reaction for the same user! User is not rewrite!
    user = User(args.username, args.password)


app_args = argparse.ArgumentParser(description="Aplikacja do zarządzania "
                                               "użytkownikami")
exclusive = app_args.add_mutually_exclusive_group(required=True)
app_args.add_argument('-p', '--password', type=str, help="Hasło użytkownika",
                      action='store', required=True)
app_args.add_argument('-n', '--new_passwd', help="Nowe hasło do zmiany",
                      action='store', type=str)
app_args.add_argument('--delete', help="Usuwanie użytkownika",
                      action='store_true', default=False)
app_args.add_argument('-e', '--edit', help="Zmiana hasła, wymagane -n",
                      action='store_true', default=False)
exclusive.add_argument('-u', '--username', help="Nazwa użytkownika",
                       action='store', type=str)
exclusive.add_argument('-l', '--list', help="Lista użytkowników",
                       action='store_true', default=False)
# TODO a help description should be change


args = app_args.parse_args()

if args.list:
    users_list()
else:
    try:
        user = User()
        user.load_by_username(args.username)
        user.authorize(args.password)
        if user.is_authorized:
            if args.edit and args.new_passwd:
                edit_user(args, user)
            elif args.delete:
                del_user(args, user)
    except ValueError:
        new_user(args)
# TODO needed to add react for error
