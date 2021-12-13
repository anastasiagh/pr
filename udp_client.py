import socket
import threading

nickname = input("Choose a nickname: ")


def receive(udp_socket_client):
    while True:
        try:
            message = udp_socket_client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print('ERROR')
            udp_socket_client.close()
            break


def write(udp_socket_client, UDP_PORT, UDP_IP):
    while True:
        message = f'{nickname}: {input("")}'
        udp_socket_client.sendtosendto(bytes(nickname, encoding='utf8'), (UDP_IP, UDP_PORT))


if __name__ == "__main__":
    UDP_IP = '127.0.0.1'
    UDP_PORT = 8001

    # udp
    udp_socket_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket_client.sendto(bytes(nickname, encoding='utf8'), (UDP_IP, UDP_PORT))

    receive_thread = threading.Thread(target=receive, args=(udp_socket_client))
    receive_thread.start()

    write_thread = threading.Thread(target=write, args=(udp_socket_client, UDP_IP, UDP_PORT))
    write_thread.start()