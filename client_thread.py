#!/usr/bin/env python
# coding:utf-8

import socket
import time
import threading
ip = 'localhost'
port = 55555


def receive(socks):
    while True:
        data = socks.recv(1024)
        print(data.decode('u8'))


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    t = threading.Thread(target=receive, args=(sock,))
    t.setDaemon(True)
    t.start()
    while 1:
        sock.send(input('>>>').encode('u8'))


if __name__ == '__main__':
    main()