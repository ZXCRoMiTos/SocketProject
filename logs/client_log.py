import logging
import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))
from main.settings import FORMAT, LOGGER_LEVEL


CLIENT_FORMATTER = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')

sys.path.append('../')
PATH = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(PATH, 'client.log')

STREAM_HANDLER = logging.StreamHandler(sys.stderr)
STREAM_HANDLER.setFormatter(CLIENT_FORMATTER)
STREAM_HANDLER.setLevel(logging.ERROR)

LOG_FILE = logging.FileHandler(PATH, encoding=FORMAT)
LOG_FILE.setFormatter(CLIENT_FORMATTER)

CLIENT_LOGGER = logging.getLogger('client')
CLIENT_LOGGER.addHandler(STREAM_HANDLER)
CLIENT_LOGGER.addHandler(LOG_FILE)
CLIENT_LOGGER.setLevel(LOGGER_LEVEL)


if __name__ == '__main__':
    CLIENT_LOGGER.critical('Критическая ошибка')
    CLIENT_LOGGER.error('Ошибка')
    CLIENT_LOGGER.debug('Информация')
    CLIENT_LOGGER.info('Сообщение')
