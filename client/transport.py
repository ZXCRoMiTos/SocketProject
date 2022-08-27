from socket import socket, AF_INET, SOCK_STREAM
from PyQt5.QtCore import QObject, pyqtSignal
from threading import Thread, Lock
from json import JSONDecodeError
import logging
import time
import sys

sys.path.append('../')
from errors import ServerError
from common.variables import *
from common.utils import *


logger = logging.getLogger('client_dist')
socket_lock = Lock()


class ClientTransport(Thread, QObject):
    new_message = pyqtSignal(str)
    connection_lost = pyqtSignal()

    def __init__(self, ip, port, database, username):
        Thread.__init__(self)
        QObject.__init__(self)
        self.address = (ip, port)
        self.database = database
        self.username = username
        self.connection()
        self.update_database()

    def connection(self):
        self.transport = socket(AF_INET, SOCK_STREAM)
        self.transport.settimeout(5)

        connected = False
        number_attempts = 5
        for try_number in range(number_attempts):
            logger.info(f'Попытка подключения №{try_number}')
            try:
                self.transport.connect(self.address)
            except (OSError, ConnectionRefusedError):
                pass
            else:
                connected = True
                break
            time.sleep(1)

        if not connected:
            error_message = 'Не удалось уставновить соединение с сервером'
            logger.critical(error_message)
            raise ServerError(error_message)

        logger.debug('Установлено соединение с сервером')

        try:
            with socket_lock:
                send_message(self.transport, self.create_presense())
                self.process_server_ans(get_message(self.transport))
        except (OSError, JSONDecodeError):
            error_message = 'Потеряно соединение с сервером'
            logger.critical(error_message)
            raise ServerError(error_message)

        logger.info('Установлено соединение с сервером')

    def create_presense(self):
        logger.debug(f'Сформировано {PRESENCE} сообщение для пользователя {self.username}')
        return {ACTION: PRESENCE, TIME: time.time(), USER: {ACCOUNT_NAME: self.username}}

    def process_server_ans(self, message):
        logger.debug(f'Разбор сообщения от сервера: {message}')
        if RESPONSE in message:
            if message[RESPONSE] == 200:
                return
            elif message[RESPONSE] == 400:
                raise ServerError(f'{message[ERROR]}')
            else:
                logger.debug(f'Принят неизвестный код подтверждения {message[RESPONSE]}')
        elif ACTION in message and message[ACTION] == MESSAGE \
                and SENDER in message and MESSAGE_TEXT in message \
                and DESTINATION in message and message[DESTINATION] == self.username:
            logger.debug(f'Получено сообщение от пользователя {message[SENDER]}: {message[MESSAGE_TEXT]}')
            self.database.save_message(message[SENDER], 'in', message[MESSAGE_TEXT])
            self.new_message.emit(message[SENDER])

    def update_database(self):
        try:
            self.user_list_update()
            self.contact_list_update()
        except OSError as err:
            if err.errno:
                error_message = 'Потеряно соединение с сервером'
                logger.critical(error_message)
                raise ServerError(error_message)
            logger.error('Timeout соединения при обновлении списков пользователей')
        except JSONDecodeError:
            error_message = 'Потеряно соединение с сервером'
            logger.critical(error_message)
            raise ServerError(error_message)
        self.running = True

    def user_list_update(self):
        logger.debug(f'Запрос списка известных пользователь {self.username}')
        request = {ACTION: USERS_REQUEST, TIME: time.time(), ACCOUNT_NAME: self.username}
        with socket_lock:
            send_message(self.transport, request)
            answer = get_message(self.transport)
        if RESPONSE in answer and answer[RESPONSE] == 202:
            self.database.add_users(answer[LIST_INFO])
        else:
            logger.error('Не удалось обновить список известных пользователей')

    def contact_list_update(self):
        logger.debug(f'Запрос контакт листа для пользователя {self.username}')
        request = {ACTION: GET_CONTACTS, TIME: time.time(), USER: self.username}
        logger.debug(f'Сформирован запрос {request}')
        with socket_lock:
            send_message(self.transport, request)
            answer = get_message(self.transport)
        logger.debug(f'Ответ получен {answer}')
        if RESPONSE in answer and answer[RESPONSE] == 202:
            for contact in answer[LIST_INFO]:
                self.database.add_contact(contact)
        else:
            logger.error('Не удалось обновить список контактов')

    def add_contact(self, contact):
        logger.debug(f'Создание контакта: {contact}')
        request = {ACTION: ADD_CONTACT, TIME: time.time(), USER: self.username, ACCOUNT_NAME: contact}
        with socket_lock:
            send_message(self.transport, request)
            self.process_server_ans(get_message(self.transport))

    def remove_contact(self, contact):
        logger.debug(f'Удаление контакта: {contact}')
        request = {ACTION: REMOVE_CONTACT, TIME: time.time(), USER: self.username, ACCOUNT_NAME: contact}
        with socket_lock:
            send_message(self.transport, request)
            self.process_server_ans(get_message(self.transport))

    def transport_shutdown(self):
        self.running = False
        exit_msg = {ACTION: EXIT, TIME: time.time(), ACCOUNT_NAME: self.username}
        with socket_lock:
            try:
                send_message(self.transport, exit_msg)
            except OSError:
                pass
        logger.debug('Сокет завершает работу')
        time.sleep(0.5)

    def send_message(self, destination, message_text):
        msg = {ACTION: MESSAGE, SENDER: self.username, DESTINATION: destination,
               TIME: time.time(), MESSAGE_TEXT: message_text}
        logger.debug(f'Сформировано сообщение: {msg}')
        with socket_lock:
            send_message(self.transport, msg)
            self.process_server_ans(get_message(self.transport))
            logger.debug(f'Сообщение отправлено пользователю {destination}')

    def run(self):
        logger.debug('Запущен процесс - прием сообщений с сервера')
        while self.running:
            time.sleep(1)
            with socket_lock:
                try:
                    self.transport.settimeout(0.5)
                    message = get_message(self.transport)
                except OSError as err:
                    if err.errno:
                        logger.critical('Потеряно соединение с сервером')
                        self.running = False
                        self.connection_lost.emmit()
                except (ConnectionError, ConnectionAbortedError, ConnectionResetError, JSONDecodeError, TypeError):
                    logger.debug('Потеряно соединение с сервером')
                    self.running = False
                    self.connection_lost.emmit()
                else:
                    logger.debug(f'Принято сообщение с сервера: {message}')
                    self.process_server_ans(message)
                finally:
                    self.transport.settimeout(5)


if __name__ == '__main__':
    pass