#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
import select

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = ("127.0.0.1", 4444)
serversocket.bind(server_address)
serversocket.listen(10)
serversocket.setblocking(False)
timeout = 10
epoll = select.epoll()
epoll.register(serversocket.fileno(), select.EPOLLIN)
message_queues = {}
fd_to_socket = {
    serversocket.fileno(): serversocket
}

while True:
    events = epoll.poll(timeout)
    if not events:
        # 无事件
        print('no event')
        continue

    for fd, event in events:
        socket = fd_to_socket[fd]

        # socket 为serversocket的时候, 为连接事件
        if socket == serversocket:
            connection, address = serversocket.accept()

            connection.setblocking(False)
            fd_to_socket[connection.fileno()] = connection
            epoll.register(connection.fileno(), select.EPOLLIN)
        # 关闭事件
        elif event & select.EPOLLHUP:
            print
            'client close'
            # 在epoll中注销客户端的文件句柄
            epoll.unregister(fd)
            # 关闭客户端的文件句柄
            fd_to_socket[fd].close()
            # 在字典中删除与已关闭客户端相关的信息
            del fd_to_socket[fd]
        # 可读事件
        elif event & select.EPOLLIN:
            # 接收数据
            data = socket.recv(1024)
            if data:
                print
                "收到数据：", data, "客户端：", socket.getpeername()
                # 将数据放入对应客户端的字典
                message_queues[socket].put(data)
                # 修改读取到消息的连接到等待写事件集合(即对应客户端收到消息后，再将其fd修改并加入写事件集合)
                epoll.modify(fd, select.EPOLLOUT)
        # 可写事件
        elif event & select.EPOLLOUT:
            try:
                # 从字典中获取对应客户端的信息
                msg = message_queues[socket].get_nowait()
            except Queue.Empty:
                print
                socket.getpeername(), " queue empty"
                # 修改文件句柄为读事件
                epoll.modify(fd, select.EPOLLIN)
            else:
                print
                "发送数据：", data, "客户端：", socket.getpeername()
                # 发送数据
                socket.send(msg)

# 在epoll中注销服务端文件句柄
epoll.unregister(serversocket.fileno())
# 关闭epoll
epoll.close()
# 关闭服务器socket
serversocket.close()

服务端代码