"""
    @author: hainq@gviet.vn
    @since: Feb 2014
"""

from twisted.internet.protocol import Protocol
from collections import deque
import struct
import msgpack
import traceback
from util.dispatcher import Dispatcher
from server_service import config
from message import Message
from database.cassandra_log import Cassandra_Log as Logger
import time
from twisted.internet import reactor


class RPC(Protocol):
    
    def __init__(self,factory):
        self.factory=factory
        
        
    def connectionMade(self):         
        Protocol.connectionMade(self)
        self.buffer=deque()
        self.request_queue=deque()
        self.factory.number_connection+=1
        print 'connection made', time.strftime("%d/%m/%Y %H:%M", time.localtime(time.time())), self.factory.number_connection

        
    def write(self,data):
        self.transport.write(data)
    
    def dataReceived(self, data):
        if not data:
            pass
            #print 'connection close'
        self.buffer.append(data)
        self.parseData()
        #self.transport.loseConnection()
        
    def connectionLost(self, reason):
        print 'reason',reason
        self.factory.number_connection-=1
        print 'connection has been lost', self.factory.number_connection
        self.buffer=None
        self.request_queue=None
            

        
    def parseData(self):
        """
            parse data come from network
            diffirent package structure need to override this method
            package struct: [4 byte length payload][payload]
            payload struct: [Type:2 byte unsign][id:4 byte unsign][Parameter:messagepack map parameter]
        """
        data=''.join(self.buffer)
        while True:
            try:
                length_data=len(data)
                if length_data > config.maximum_package_size:
                    raise Exception("Bad request: size of package too large", length_data)
                if length_data < 4:
                    return
                else:
                    length_payload,=struct.unpack("!I",data[0:4])
                    if length_payload > config.maximum_package_size:
                        self.buffer.append(data)
                        raise Exception("Bad request: Payload length to large", length_payload)
                    length_package= 4 + length_payload
                    if length_data < length_package:
                        self.buffer.append(data)
                        return
                    else:
                        payload=data[4:length_package]
                        data=data[length_package:]    
                        self.buffer.clear()
                        if data:
                            self.buffer.append(data)  
                        mess=Message(payload)
                        dispatcher=Dispatcher.get_dispatcher()
                        dispatcher.call(mess.get_type(),mess.get_id(),self,mess.get_data())
                        if config.log_to_cassandra:
                            reactor.callFromThread(Logger.get_instance().log_request,payload)
            except:
                if config.log_to_cassandra:
                    reactor.callFromThread(Logger.get_instance().log_err, traceback.format_exc())
                else:
                    print time.strftime("%d/%m/%Y %H:%M", time.localtime(time.time())), traceback.format_exc()
                self.transport.loseConnection()
                return
        
        
    