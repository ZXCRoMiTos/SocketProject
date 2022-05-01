from main.common_functions import receive_message, send_message, create_address
from main.settings import DEFAULT_ANSWERS, MAX_CONNECTIONS
import socket
import json


def server_start():
    print('[SERVER] Server is run...')
    server.listen(MAX_CONNECTIONS)
    while True:
        client, address = server.accept()
        print(f'[SERVER] Connection with {address[0]}:{address[1]}.')
        message = receive_message(client)
        print(f'[SERVER] Message received - {message}.')
        action = message['action']
        if action == 'presence':
            response = DEFAULT_ANSWERS['presence']
            print(f'[SERVER] Message send - {json.dumps(response, ensure_ascii=False)}.')
            send_message(client, response)
        else:
            response = DEFAULT_ANSWERS['error']
            print(f'[SERVER] Unknown action - {action}.')
            send_message(client, response)


if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(create_address())
    server_start()
