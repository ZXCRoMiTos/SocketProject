import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))
from logs_config import client_log, server_log
import logging
import inspect
import traceback


flag = inspect.stack()[-1].filename
if flag == 'client.py':
    LOGGER = logging.getLogger('client')
elif flag == 'server.py':
    LOGGER = logging.getLogger('server')


def log(func):
    def wrapper(*args):
        filename = inspect.stack()[-1].filename
        calling_functions = traceback.format_stack()[0].strip().split()[-1]
        LOGGER.debug(f'{filename} - {calling_functions} - {func.__name__} - {args}', stacklevel=2)
        return func(*args)
    return wrapper


class Log:
    def __call__(self, func):
        def wrapper(*args):
            filename = inspect.stack()[-1].filename
            calling_functions = traceback.format_stack()[0].strip().split()[-1]
            LOGGER.debug(f'{filename} - {calling_functions} - {func.__name__} - {args}', stacklevel=2)
            return func(*args)
        return wrapper
