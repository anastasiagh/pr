import socket
import os
import threading
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from flask import Flask, request

clients = {}
addresses = {}


def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


def handle_client(client):
    name = client.recv(1024).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(1024)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break


def accept_incoming_connections():
    # Sets up handling for incoming clients.
    while True:
        client, client_address = server.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the chat app! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def http_server():
    app.run(host=host, port=HTTP_port)


app = Flask(__name__)


@app.route('/', methods=['POST'])
def result():
    app_root = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(app_root, 'static/files/')
    if not os.path.isdir(target):
        os.makedirs(target)
    print(request.files['file'])
    file = request.files['file']
    file_name = file.filename or ''
    destination = '/'.join([target, file_name])
    file.save(destination)
    f = open(destination, 'rb')
    l = f.read(1024)
    msg = "/send file:" + file_name
    broadcast(bytes(msg, "utf8"))
    while (l):
        for client in clients:
            name = clients[client]
            broadcast(l, name + ": ")
            print('Sent ', repr(l))
            l = f.read(1024)
    f.close()

    print('Done sending')
    return 'Received !'  # response to your request.


if __name__ == "__main__":
    host = "127.0.0.1"
    TCP_port = 8000
    HTTP_port = 8004
    # tcp
    server = socket(AF_INET, SOCK_STREAM)

    # udp
    # server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server.bind((host, TCP_port))
    server.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    http_thread = Thread(target=http_server)
    ACCEPT_THREAD.start()
    http_thread.start()
    ACCEPT_THREAD.join()
    server.close()
