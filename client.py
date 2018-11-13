#!/usr/bin/env python
# coding:utf-8

import socket
import time


ip = 'localhost'
port = 55555


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(sock)
    sock.connect((ip, port))
    print(sock)
    while 1:
        data = sock.recv(1024)
        if not data:
            raise Exception('socket closed')


if __name__ == '__main__':
    main()