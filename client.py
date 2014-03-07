# coding= utf-8
import socket
import os
import time
import struct
import threading
import traceback
import msgpack
#from server_service.server.message import Message

'a'

body_data={'x':10,'y':40,'method':'hainq'}
I=struct.Struct('!i')
H=struct.Struct('!H')
i=0
#logging.basicConfig(filename='log_client', level=logging.DEBUG, filemode="w")
def client_connect():
    print 'client_connect'
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#    client.connect(('10.2.10.156',9002))
    client.connect(('localhost',9001))
    client.send('xxxxxx')
    #client.close()
    while True:
        print '..'
        time.sleep(2)

    
if __name__=='__main__':
    list1=[]
    start=time.time()
    for i in range(5):
        th=threading.Thread(target=client_connect)
        th.setDaemon(True)
        th.start()
        list1.append(th)
    finish=time.time()
    while True:
        time.sleep(5)
