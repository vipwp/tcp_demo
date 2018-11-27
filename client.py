#!/usr/bin/env python
# coding:utf-8

import socket

ip = 'localhost'
port = 55555


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    while 1:
        data = sock.recv(1024)
        if not data:
            raise Exception('socket closed')
        print(data)
        sock.send(('received:' + data.decode('u8')).encode('u8'))


if __name__ == '__main__':
    main()