#!/usr/bin/env python
# coding:utf-8

import socket

ip = 'localhost'
port = 55555


clients = []


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, port))
    sock.listen(1)

    while True:
        print('listening...')
        client_sock, address = sock.accept()
        print('new client:', address, client_sock)
        clients.append(client_sock)
        client_sock.send('welcome'.encode('u8'))
        print(client_sock.recv(1024))


if __name__ == '__main__':
    main()