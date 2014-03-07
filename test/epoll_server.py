# coding= utf-8
"""
    selector for event server base
    use epoll system call for best performance
    @requires: Linux 2.5 +
    @author: hainq@gviet.vn

"""
import select
import threading
import logging
import time
import traceback
import sys
import socket

print 'select.EPOLLERR:', select.EPOLLERR
print 'select.EPOLLIN:',  select.EPOLLIN
print 'select.EPOLLHUP:', select.EPOLLHUP
print 'select.EPOLLOUT:', select.EPOLLOUT

def ping(socket_):
    print 'ping'
    socket_.send('ping');

if __name__=='__main__':
    list_socket={}
    epoll=select.epoll()
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.setblocking(False)
    server.bind(('localhost',9002))
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.listen(5)
    epoll.register(server.fileno(),select.EPOLLIN)
    EDISCONNECT= select.EPOLLHUP | select.EPOLLERR
    i=0
    while True:
        
        print 'poll','i=',i
        i+=1
        for fd,event in epoll.poll(60):
            
            if fd==server.fileno():
                print 'client accept'
                client,addr=server.accept()
                epoll.register(client.fileno(), select.EPOLLIN |  EDISCONNECT)
                list_socket[client.fileno()]=client
                print 'len client', len(list_socket)
            else:
                if event & select.EPOLLIN:
                    print 'event read'
                    try:
                        data=list_socket[fd].recv(1024)
                    except:
                        data=''
                    if not data:
                        list_socket[fd].close()
                        del list_socket[fd]
                        epoll.unregister(fd)
                        print '		data is None, length client=', len(list_socket) 
                else:
                    print 'event #', fd, event     
                    list_socket[fd].close()
                    del list_socket[fd] 
                    epoll.unregister(fd)
                    #time.sleep(3)
        if i%6==0:
            for fd in list_socket:
                if fd != server.fileno():
                    try:
                        ping(list_socket[fd])
                    except:
                        print traceback.format_exc()
                
        
