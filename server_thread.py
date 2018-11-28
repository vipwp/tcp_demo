#!/usr/bin/env python
# coding:utf-8

import socket
import threading
import time
import datetime

ip = 'localhost'
port = 55555


clients = []


def tick():
    while True:
        for _ in clients:
            _.send(str(datetime.datetime.now()).encode('u8'))
        time.sleep(2)


def process(client_sock):
    clients.append(client_sock)
    client_sock.send('welcome'.encode('u8'))
    while True:
        try:
            data = client_sock.recv(1024)
            print(data)
            client_sock.send(b'echo: ' + data)
        except:
            clients.remove(client_sock)
            client_sock.close()


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, port))
    print('listening...')
    sock.listen(1)

    tt = threading.Thread(target=tick)
    tt.setDaemon(True)
    tt.start()

    while True:
        client_sock, address = sock.accept()
        print('new client:', address, client_sock)
        t = threading.Thread(target=process, args=(client_sock, ))
        t.setDaemon(True)
        t.start()


if __name__ == '__main__':
    main()