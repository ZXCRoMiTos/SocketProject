from .settings import FORMAT, MESSAGE_SIZE, DEFAULT_IP, DEFAULT_PORT
from .decorators import log, Log
import json
import sys
import re


@log
def decode_message(message):
    if isinstance(message, bytes):
        decoded_message = json.loads(message.decode(FORMAT))
        if isinstance(decoded_message, dict):
            return decoded_message
        raise ValueError
    raise ValueError


@Log()
def encode_message(message):
    if isinstance(message, dict):
        return json.dumps(message, ensure_ascii=False).encode(FORMAT)
    raise TypeError


@log
def receive_message(client):
    return decode_message(client.recv(MESSAGE_SIZE))


@Log()
def send_message(client, message):
    client.send(encode_message(message))


@log
def is_ip(address):
    try:
        pattern = "([0-9]{1,3}[\.]){3}[0-9]{1,3}"
        if re.search(pattern, address):
            return True
    except TypeError:
        return False


@Log()
def create_address():

    if '-ip' in sys.argv:
        input_ip = sys.argv[sys.argv.index('-ip') + 1]
        if is_ip(input_ip):
            ip = input_ip
        else:
            print('После "-ip" нужно указать IP адрес.')
            exit(1)
    else:
        ip = DEFAULT_IP

    try:
        if '-p' in sys.argv:
            num = int(sys.argv[sys.argv.index('-p') + 1])
            if 1024 <= num <= 65535:
                port = num
            else:
                print('Нужно указать порт в диапазоне 1024 - 65535.')
                exit(2)
        else:
            port = DEFAULT_PORT
    except ValueError:
        print('После "-p" нужно указать порт.')
        exit(3)

    return ip, port
