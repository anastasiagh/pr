import socket
import threading

nickname = input("Choose a nickname: ")


def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print('ERROR')
            client.close()
            break


def write():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))


if __name__ == "__main__":
    # tcp
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # udp
    # client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    client.connect(('127.0.0.1', 8000))

    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()