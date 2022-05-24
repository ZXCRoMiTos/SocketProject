from main.common_functions import send_message, receive_message, create_address
import logs_config.client_log
import logging
import socket
import json
import time


CLIENT_LOGGER = logging.getLogger('client')


def answer_parsing(message):
    print('code:', message.get('response'))
    print('alert:', message.get('alert'))


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = create_address()
    client.connect(address)

    CLIENT_LOGGER.debug(f'Client connect to {address}')

    msg = {
        "action": "presence",
        "time": time.time(),
        "type": "status",
        "user": {
            "account_name": "guest",
            "status": "I'm here"
        }
    }

    send_message(client, msg)
    CLIENT_LOGGER.debug(f'Client send {json.dumps(msg)} to {address}')
    message = receive_message(client)
    CLIENT_LOGGER.debug(f'Client receive message {json.dumps(message)} from {address} ')
    answer_parsing(message)


if __name__ == '__main__':
    main()