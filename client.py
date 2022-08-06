from main.common_functions import send_message, receive_message, create_address
from main.decorators import log, Log
import logs_config.client_log
import threading
import logging
import socket
import json
import time
from datetime import date
import sys


@log
def handshake():
    first_msg = {
        "action": "presence",
        "time": time.time(),
        "type": "status",
        "user": {
            "account_name": get_name(),
            "status": "I'm here"
        }
    }

    send_message(client, first_msg)
    CLIENT_LOGGER.debug(f'Client send {json.dumps(first_msg)} to {address}')
    answer = receive_message(client)
    CLIENT_LOGGER.debug(f'Client receive message {json.dumps(answer)} from {address} ')
    parsing_answer(answer)


@Log()
def parsing_answer(message):
    action = message.get('action')
    if action == 'presence':
        print(f'Установлено соединение с сервером {address}, {message.get("response")}.')
    elif action == 'message':
        messages.append(f'\n{date.today()} | Получено сообщение от {message.get("account_name")}, сообщение: \n"{message.get("message_text")}".\n')
    elif action == 'error':
        print(f'Произошла ошибка, {message.get("response")}.')
    else:
        print(f'Неизвестный action - {action}.')


@log
def create_message():
    receiver_name = input('\nВведите имя получателя, если хотите выйти введите q: ')
    if receiver_name == 'q':
        return
    message = input('Введите сообщение, если хотите выйти введите q: ')
    if message == 'q':
        return

    message_dict = {
        'action': 'message',
        'time': time.time(),
        'account_name': get_name(),
        'from': receiver_name,
        'message_text': message
    }

    CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


@log
def show_messages():
    if messages:
        for message in messages:
            print(message)
    else:
        print('Нет сообщений :C')


@Log()
def get_name():
    if '-name' in sys.argv:
        name = sys.argv[sys.argv.index('-name') + 1]
        return name
    exit(1)


@log
def listen_server():
    while True:
        try:
            parsing_answer(receive_message(client))
        except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
            CLIENT_LOGGER.error(f'Соединение с сервером {address} было потеряно.')
            sys.exit(1)


@log
def user_interface():
    print(f'Здравствуйте, {get_name()}')
    print('Введите send для отправки сообщения')
    print('Введите messages для просмотра сообщений')
    print('Введите exit для выхода')
    while True:
        try:
            action = input('\nВведите действие: ')
            if action == 'send':
                try:
                    send_message(client, create_message())
                except TypeError:
                    pass
            elif action == 'messages':
                show_messages()
            elif action == 'exit':
                client.close()
                CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
                sys.exit(0)
        except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
            CLIENT_LOGGER.error(f'Соединение с сервером {address} было потеряно.')
            sys.exit(1)


def start():
    handshake()
    receiver = threading.Thread(target=listen_server, args=[], daemon=True)
    sender = threading.Thread(target=user_interface, args=[], daemon=True)
    receiver.start()
    sender.start()
    while True:
        time.sleep(1)
        if receiver.is_alive() and sender.is_alive():
            continue
        break


if __name__ == '__main__':
    CLIENT_LOGGER = logging.getLogger('client')
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    address = create_address()
    client.connect(address)
    CLIENT_LOGGER.debug(f'Client connect to {address}')
    messages = []
    start()
