DEFAULT_IP = '127.0.0.1'
DEFAULT_PORT = 7777
MAX_CONNECTIONS = 5

FORMAT = 'utf-8'
MESSAGE_SIZE = 640
DEFAULT_ANSWERS = {
    'presence': {
        "response": 200,
        "alert": "Success"
    },
    'error': {
        "response": 400,
        "alert": "Bad request"
    }
}
