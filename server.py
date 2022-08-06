from main.common_functions import receive_message, send_message, create_address
from main.settings import DEFAULT_ANSWERS, MAX_CONNECTIONS
from main.decorators import log, Log
import logs_config.server_log
import logging
import socket
import select
import json
import time


SERVER_LOGGER = logging.getLogger('server')


@log
def give_answer(client, messages, names):
    message = receive_message(client)
    SERVER_LOGGER.debug(f'Message received - {message}.')
    action = message['action']
    if action == 'presence':
        if message['user']['account_name'] not in names:
            names[message['user']['account_name']] = client
            response = DEFAULT_ANSWERS['presence']
            SERVER_LOGGER.debug(f'Message send - {json.dumps(response, ensure_ascii=False)}.')
            send_message(client, response)
        else:
            response = DEFAULT_ANSWERS['error']
            SERVER_LOGGER.debug(f'Unknown action - {action}.')
            send_message(client, response)
    elif action == 'message':
        messages.append(message)
    else:
        response = DEFAULT_ANSWERS['error']
        SERVER_LOGGER.debug(f'Unknown action - {action}.')
        send_message(client, response)


@log
def send_message_for_user(message, names, listeners):
    if message['from'] in names and names[message['from']] in listeners:
        client_socket = names[message['from']]
        send_message(client_socket, message)


@log
def get_key(names, value):
    for k, v in names.items():
        if v == value:
            return k


def server_start():
    print('Server is run...')
    SERVER_LOGGER.debug('Server is run...')
    clients = []
    messages = []
    names = {}
    while True:
        try:
            client, address = server.accept()
            SERVER_LOGGER.debug(f'Connection with {address[0]}:{address[1]}.')
        except OSError:
            pass
        else:
            print(f'Установлено соедение с ПК {address}')
            SERVER_LOGGER.debug(f'Установлено соедение с ПК {address}')
            clients.append(client)

        rec_data = []
        send_data = []
        err = []

        try:
            if clients:
                rec_data, send_data, err = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if rec_data:
            for cl in rec_data:
                try:
                    give_answer(cl, messages, names)
                except Exception:
                    clients.remove(cl)
                    del names[get_key(names, cl)]

        for message in messages:
            send_message_for_user(message, names, send_data)
        messages.clear()


if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(create_address())
    server.listen(MAX_CONNECTIONS)
    server.settimeout(0.5)
    server_start()
