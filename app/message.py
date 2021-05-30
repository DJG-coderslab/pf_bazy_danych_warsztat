#!python
# encoding: utf-8

# Created by djg-m at 09.01.2021

import argparse

from models import Message, User


def messages_list(user):
    """
    Prints all messages for one specified user.

    :param user: specified for user User object
    :type user: User
    :return: None
    :rtype: None
    """
    msg = Message()
    messages = msg.load_by_receiver(user.id)
    for message in messages:
        sender = User()
        sender.load_by_id(message.from_id)
        print(f"{message.creation_date} | {sender.username} | "
              f"{message.message}")


def send_message(args, user):
    """
    Sends a new message from fogged user

    :param args: object with CLI arguments
    :type args: args
    :param user: object for logged user
    :type user: user
    :return: None
    :rtype: None
    """
    receiver = User()
    receiver.load_by_username(args.to)
    message = Message()
    message.new_message(user.id, receiver.id, args.send)


app_args = argparse.ArgumentParser(description="Aplikacja do zarządzania "
                                               "wiadomościami")
app_args.add_argument('-p', '--password', type=str, help="Hasło użytkownika",
                      action='store', required=True)
app_args.add_argument('-t', '--to', help="Nazwa odbiorcy wiadomości",
                      action='store', type=str)
app_args.add_argument('-s', '--send', help="Treść wiadomości",
                      action='store', type=str)
app_args.add_argument('-u', '--username', help="Nazwa użytkownika",
                      action='store', type=str)
app_args.add_argument('-l', '--list', help="Lista użytkowników",
                      action='store_true', default=False)

args = app_args.parse_args()

try:
    user = User()
    user.load_by_username(args.username)
    user.authorize(args.password)
    if user.is_authorized:
        if args.list:
            messages_list(user)
        elif args.to and args.send:
            send_message(args, user)
except ValueError:
    pass
