from .settings import FORMAT, MESSAGE_SIZE, DEFAULT_IP, DEFAULT_PORT
import json
import sys


def decode_message(message):
    if isinstance(message, bytes):
        decoded_message = json.loads(message.decode(FORMAT))
        if isinstance(decoded_message, dict):
            return decoded_message
        raise ValueError
    raise ValueError


def encode_message(message):
    return json.dumps(message, ensure_ascii=False).encode(FORMAT)


def receive_message(client):
    return decode_message(client.recv(MESSAGE_SIZE))


def send_message(client, message):
    client.send(encode_message(message))


def create_address():

    try:
        if '-ip' in sys.argv:
            ip = sys.argv[sys.argv.index('-ip') + 1]
        else:
            ip = DEFAULT_IP
    except IndexError:
        print('После "-ip" нужно указать IP адрес.')
        exit(1)
    try:
        if '-p' in sys.argv:
            num = int(sys.argv[sys.argv.index('-p') + 1])
            if 1024 <= num <= 65535:
                port = num
            else:
                raise ValueError
        else:
            port = DEFAULT_PORT
    except IndexError:
        print('После "-p" нужно указать порт.')
        exit(2)
    except ValueError:
        print('Нужно указать порт в диапазоне 1024 - 65535.')
        exit(3)

    return ip, port