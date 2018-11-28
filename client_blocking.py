#!/usr/bin/env python
# coding:utf-8

import socket

ip = 'localhost'
port = 55555


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    while 1:
        try:
            data = sock.recv(1024)
        except:
            data = None
        if not data:
            raise Exception('socket closed')
        sock.send(input('>>>').encode('u8'))
        # sock.send(pickle.dumps('received:' + pickle.loads(data)))
        print(b'from server: ' + data)


if __name__ == '__main__':
    main()