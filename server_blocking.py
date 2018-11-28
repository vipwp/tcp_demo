#!/usr/bin/env python
# coding:utf-8

import socket

ip = 'localhost'
port = 55555


clients = []


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, port))
    print('listening...')
    sock.listen(1)
    client_sock, address = sock.accept()
    print('new client:', address, client_sock)
    while True:
        clients.append(client_sock)
        client_sock.send('welcome'.encode('u8'))
        data = client_sock.recv(1024)
        print(data)
        client_sock.send(b'echo: ' + data)


if __name__ == '__main__':
    main()