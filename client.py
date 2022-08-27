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
from PyQt5.QtWidgets import QApplication
from client.client_gui import StartDialog, ClientMainWindow
from client.transport import ClientTransport


logger = logging.getLogger('client_dist')


@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-n', '--name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_name = namespace.name

    if not 1023 < server_port < 65536:
        logger.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. Допустимы адреса с 1024 до 65535. Клиент завершается.')
        exit(1)

    return server_address, server_port, client_name


if __name__ == '__main__':
    server_address, server_port, client_name = arg_parser()
    client_app = QApplication(sys.argv)
    if not client_name:
        start_dialog = StartDialog()
        client_app.exec_()
        if start_dialog.ok_pressed:
            client_name = start_dialog.client_name.text()
            del start_dialog
        else:
            exit(0)

    logger.info(f'Запущен клиент'
                f' Адрес сервера - {server_address}:{server_port}'
                f' Имя клиента - {client_name}')

    database = ClientStorage(client_name)

    try:
        transport = ClientTransport(server_address, server_port, database, client_name)

    except ServerError as error:
        print(error.text)
        exit(1)
    transport.setDaemon(True)
    transport.start()

    main_window = ClientMainWindow(database, transport)
    main_window.make_connection(transport)
    main_window.setWindowTitle(f'Мессенджер | {client_name}')
    client_app.exec_()

    transport.transport_shutdown()
    transport.join()
