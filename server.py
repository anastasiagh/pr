import socket
import threading
import http.server

clients = []
nicknames = []
clients_udp = []
udp_socket = None


def broadcast(message, udp_socket=None):
    for client in clients:
        client.send(message)
    if udp_socket:
        for udp_client in clients_udp:
            udp_socket.sendto(bytes(message, encoding='utf8'), (udp_client))


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = client.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat..".encode('ascii'))
            nicknames.remove(nickname)
            break


def handle_udp(address_udp, udp_socket):
    while True:
        try:
            message = udp_socket.recvfrom(1024)
            broadcast(message, udp_socket)
        except:
            index = clients_udp.index(address_udp[0])
            nickname = nicknames[index]
            clients_udp.remove(address_udp)
            broadcast(f"{nickname} left the chat..".encode('ascii'), udp_socket)
            nicknames.remove(nickname)
            break


def server_tcp_start(HOST, TCP_PORT):
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((HOST, TCP_PORT))
    tcp_socket.listen(10)
    client, address = tcp_socket.accept()
    print(f"Connection established with TCP- {client}:{address}")
    print(f"connected with {str(address)} ")
    client.send('NICK'.encode('ascii'))
    nickname = client.recv(1024).decode('ascii')
    nicknames.append(nickname)
    clients.append(client)
    print(f'Nickname is {nickname}')
    broadcast(f'{nickname} joined the chat'.encode('ascii'))
    client.send('Connected to the server'.encode('ascii'))
    thread = threading.Thread(target=handle, args=(client,))
    thread.start()


def server_udp_start(HOST, UDP_PORT):
    global udp_socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((HOST, UDP_PORT))
    print("UDP server up and listening")
    nickname, address_udp = udp_socket.recvfrom(1024)
    print(address_udp)
    print("\n" + nickname.decode("utf-8"))
    nicknames.append(nickname.decode("utf-8"))
    clients_udp.append(address_udp[0])
    print(f'Nickname is {nickname.decode("utf-8")}')
    print(type(nickname))
    print(type(address_udp))
    broadcast(f'{nickname.decode("utf-8")} joined the chat', udp_socket)
    udp_socket.sendto(bytes(nickname.decode("utf-8"), encoding='utf8'), (HOST, UDP_PORT))
    thread = threading.Thread(target=handle_udp, args=(address_udp))
    thread.start()


if __name__ == "__main__":
    HOST = "127.0.0.1"
    TCP_PORT = 8000
    UDP_PORT = 8001
    HTTP_PORT = 8002
    # tcp
    #  tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #  tcp_socket.bind((HOST, TCP_PORT))
    # udp
    #  udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #  udp_socket.bind((HOST, UDP_PORT))
    # http
    # http_server = http.server.HTTPServer((HOST, HTTP_PORT), HttpHandler)

    print("Start server")
    tcp_tread = threading.Thread(target=server_tcp_start, args=(HOST, TCP_PORT))
    udp_thread = threading.Thread(target=server_udp_start, args=(HOST, UDP_PORT))
    #  http_thread = threading.Thread(target=server_http_start, args=(http_server))

    tcp_tread.start()
    udp_thread.start()
#  http_thread.start()
