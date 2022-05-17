import logging.handlers
import logging
import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))
from main.settings import FORMAT, LOGGER_LEVEL


SERVER_FORMATTER = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')

sys.path.append('../')
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'server.log')

STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(SERVER_FORMATTER)
STREAM_HANDLER.setLevel(logging.ERROR)

LOG_FILE = logging.handlers.TimedRotatingFileHandler(PATH, encoding=FORMAT, interval=1, when='D')
LOG_FILE.setFormatter(SERVER_FORMATTER)

SERVER_LOGGER = logging.getLogger('server')
SERVER_LOGGER.addHandler(STREAM_HANDLER)
SERVER_LOGGER.addHandler(LOG_FILE)
SERVER_LOGGER.setLevel(LOGGER_LEVEL)


if __name__ == '__main__':
    SERVER_LOGGER.critical('Критическая ошибка')
    SERVER_LOGGER.error('Ошибка')
    SERVER_LOGGER.debug('Информация')
    SERVER_LOGGER.info('Сообщение')
