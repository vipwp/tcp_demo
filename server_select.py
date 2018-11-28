#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import select
import pickle
import datetime
import time

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  #设置端口复用，这样重启服务的时候，不用等待1分钟
server_address = ("0.0.0.0", 4444)
serversocket.bind(server_address)
serversocket.listen(10)
serversocket.setblocking(False)
timeout = 1
clients = []
buffer_size = 1024

name_mapping = {}


def send_to_all(msg, from_sock=None, to_sock=None, mtype='msg'):
    if to_sock:
        _clients = [to_sock]
    else:
        _clients = clients
    for _ in _clients:
        if from_sock is not _:
            _.send(msg if type(msg) == bytes else pickle.dumps({mtype: msg}))


def read_socket(socks):
    data = b''
    while True:
        _data = socks.recv(buffer_size)
        data += _data
        data_len = len(_data)
        if data_len == 0:
            break
        else:
            if data_len < buffer_size:
                break
    return data


def build_name(address):
    return '{}:{}'.format(address[0], address[1])


def disconnect(socks):
    socks.close()
    clients.remove(socks)
    msg = '用户（{}）已经离开'.format(name_mapping.get(socks))
    del name_mapping[socks]
    send_to_all(msg)


duration = timeout
_timeout = timeout


while True:
    if (_timeout - duration) < 0.01:
        _timeout = 1
    else:
        _timeout = timeout - duration
    print(duration, _timeout)
    start = time.time()
    readable_socks, writeable_socks, exception_socks = select.select(clients + [serversocket], [], clients, _timeout)
    for socks in readable_socks:

        if socks == serversocket:
            connection, address = serversocket.accept()

            connection.setblocking(False)
            connection.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            clients.append(connection)

            name_mapping[connection] = address
            send_to_all('{}'.format(build_name(address)), to_sock=connection, mtype='id')
            msg = '欢迎用户（{}）加入'.format(address)
            send_to_all(msg)

        else:
            try:
                data = read_socket(socks)
            except Exception as e:
                print(e)
                data = None
            if data is not None:
                address = name_mapping.get(socks)
                print("收到数据：", data, "客户端：", )
                msg = '{}:{}'.format(build_name(address), pickle.loads(data))
                send_to_all(msg)

            else:
                disconnect(socks)

    for socks in exception_socks:
        if socks in clients:
            disconnect(socks)

    send_to_all('服务器时间：' + str(datetime.datetime.now())[:-7], mtype='status')
    duration = time.time() - start


serversocket.close()
