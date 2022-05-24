from main.common_functions import receive_message, send_message, create_address
from main.settings import DEFAULT_ANSWERS, MAX_CONNECTIONS
import logs_config.server_log
import logging
import socket
import json


SERVER_LOGGER = logging.getLogger('server')


def server_start():
    SERVER_LOGGER.debug('Server is run...')
    server.listen(MAX_CONNECTIONS)
    while True:
        client, address = server.accept()
        SERVER_LOGGER.debug(f'Connection with {address[0]}:{address[1]}.')
        message = receive_message(client)
        SERVER_LOGGER.debug(f'Message received - {message}.')
        action = message['action']
        if action == 'presence':
            response = DEFAULT_ANSWERS['presence']
            SERVER_LOGGER.debug(f'Message send - {json.dumps(response, ensure_ascii=False)}.')
            send_message(client, response)
        else:
            response = DEFAULT_ANSWERS['error']
            SERVER_LOGGER.debug(f'Unknown action - {action}.')
            send_message(client, response)


if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(create_address())
    server_start()
