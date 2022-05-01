import subprocess


PROCESS = []

while True:

    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, c - запустить клиенты, x - закрыть все окна: ')

    if ACTION == 'q':
        break

    elif ACTION == 's':
        PROCESS.append(subprocess.Popen('python server.py',
                                        creationflags=subprocess.CREATE_NEW_CONSOLE))
        for _ in range(5):
            PROCESS.append(subprocess.Popen('python client.py',
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))
    elif ACTION == 'c':
        for _ in range(5):
            PROCESS.append(subprocess.Popen('python client.py',
                                            creationflags=subprocess.CREATE_NEW_CONSOLE))

    elif ACTION == 'x':
        while PROCESS:
            VICTIM = PROCESS.pop()
            VICTIM.kill()
