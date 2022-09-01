import socket
import time
import argparse
import threading
from common.variables import *
from common.utils import *
from errors import IncorrectDataRecivedError, ReqFieldMissingError, ServerError
from decos import log
import dis
from SocketProject.client.client_database import ClientStorage
from PyQt5.QtWidgets import QApplication, QMessageBox
from client.client_gui import StartDialog, ClientMainWindow
from client.transport import ClientTransport


logger = logging.getLogger('client_dist')


@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    parser.add_argument('-p', '--password', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name
    client_password = namespace.password

    if not 1023 < server_port < 65536:
        logger.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        exit(1)

    return server_address, server_port, client_name, client_password


if __name__ == '__main__':
    server_address, server_port, client_name, client_password = arg_parser()
    client_app = QApplication(sys.argv)

    start_dialog = StartDialog()
    if not client_name or not client_password:
        client_app.exec_()
        if start_dialog.ok_pressed:
            client_name = start_dialog.client_name.text()
            client_password = start_dialog.client_password.text()
            logger.debug(f'USING | USERNAME: {client_name}, PASSWORD: {client_password}')
        else:
            exit(0)

    logger.info(f'Запущен клиент'
                f' Адрес сервера - {server_address}:{server_port}'
                f' Имя клиента - {client_name}')

    database = ClientStorage(client_name)

    try:
        transport = ClientTransport(server_address, server_port, database, client_name, client_password)
        logger.debug('Transport started work')
    except ServerError as error:
        message = QMessageBox()
        message.critical(start_dialog, 'Ошибка', error.text)
        exit(1)
    transport.setDaemon(True)
    transport.start()

    del start_dialog

    main_window = ClientMainWindow(database, transport)
    main_window.make_connection(transport)
    main_window.setWindowTitle(f'Мессенджер | {client_name}')
    client_app.exec_()

    transport.transport_shutdown()
    transport.join()
