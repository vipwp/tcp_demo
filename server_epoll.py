#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import select
import pickle

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  #设置端口复用，这样重启服务的时候，不用等待1分钟
server_address = ("127.0.0.1", 4444)
serversocket.bind(server_address)
serversocket.listen(10)
serversocket.setblocking(False)
timeout = 1
epoll = select.epoll()
epoll.register(serversocket.fileno(), select.EPOLLIN)
message_queues = {}
fd_to_socket = {
    serversocket.fileno(): serversocket
}
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


def send_to_all(msg, client_sock=None):
    for _ in clients:
        if client_sock is not _:
            _.send(msg if type(msg) == bytes else pickle.dumps(msg))


def disconnect(fd):

    epoll.unregister(fd)
    client_sock = fd_to_socket[fd]
    # 关闭客户端的文件句柄
    client_sock.close()
    # 在字典中删除与已关闭客户端相关的信息
    del fd_to_socket[fd]
    clients.remove(client_sock)
    msg = '用户（{}）已经离开'.format(build_name(name_mapping[client_sock]))
    del name_mapping[socks]
    send_to_all(msg)

while True:
    events = epoll.poll(timeout)
    if not events:
        # 无事件
        print('no event')
        continue

    for fd, event in events:
        socks = fd_to_socket[fd]

        # socket 为serversocket的时候, 为连接事件
        if socks == serversocket:
            connection, address = serversocket.accept()

            connection.setblocking(False)
            fd_to_socket[connection.fileno()] = connection
            epoll.register(connection.fileno(), select.EPOLLIN)
            name_mapping[connection] = address
            clients.append(connection)

            send_to_all('{}'.format(build_name(address)), to_sock=connection, mtype='id')

            msg = '欢迎用户（{}）加入'.format(build_name(address))
            send_to_all(msg)

        # 关闭事件
        elif event & select.EPOLLHUP:
            disconnect(fd)

        # 可读事件
        elif event & select.EPOLLIN:
            # 接收数据
            data = read_socket(socks)
            if data:
                print("收到数据：", data, "客户端：", name_mapping[socks])
                msg = '{}:{}'.format(build_name(name_mapping[socks]), pickle.loads(data))
                send_to_all(msg, socks)

                # 将数据放入对应客户端的字典
                # message_queues[socket].put(data)
                # 修改读取到消息的连接到等待写事件集合(即对应客户端收到消息后，再将其fd修改并加入写事件集合)
                # epoll.modify(fd, select.EPOLLOUT)
        # # 可写事件
        # elif event & select.EPOLLOUT:
        #     try:
        #         # 从字典中获取对应客户端的信息
        #         msg = message_queues[socket].get_nowait()
        #     except Queue.Empty:
        #         print
        #         socket.getpeername(), " queue empty"
        #         # 修改文件句柄为读事件
        #         epoll.modify(fd, select.EPOLLIN)
        #     else:
        #         print
        #         "发送数据：", data, "客户端：", socket.getpeername()
        #         # 发送数据
        #         socket.send(msg)


epoll.unregister(serversocket.fileno())
epoll.close()
serversocket.close()
