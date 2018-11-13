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
        client_sock, address = sock.accept()
        print(address, client_sock)
        clients.append(client_sock)
        print(client_sock.recv(1024))
        # client_sock.send(b'test_message')
        # client_sock.close()


if __name__ == '__main__':
    main()