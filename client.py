from main.common_functions import send_message, receive_message, create_address
import socket
import time


def answer_parsing(message):
    print('code:', message.get('response'))
    print('alert:', message.get('alert'))


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(create_address())

    msg = {
        "action": "presence",
        "time": time.time(),
        "type": "status",
        "user": {
            "account_name": "guest",
            "status": "I'm here"
        }
    }

    send_message(client, msg)
    answer_parsing(receive_message(client))


if __name__ == '__main__':
    main()