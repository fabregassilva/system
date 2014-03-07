"""
    @author: hainq@gviet.vn
    @since: Feb 2014
    @last update: Feb 2014
"""
import sys
from twisted.internet.task import LoopingCall
sys.path.append('/home/hai/Documents/Aptana/')
#print sys.path
from twisted.internet.protocol import ServerFactory
from twisted.internet.protocol import Protocol
from server_service import config
from server_service.network.message import Message
from twisted.internet.protocol import ClientFactory
from collections import deque
import struct
import traceback
from twisted.internet.defer import Deferred
import time
from twisted.internet import reactor
import sys
from twisted.internet import task
import random

log_user={'logtype':1,'app_id':2,'username':'hainq','contents':"Hainq test user log fhgdfhghjdfghdf", 'response':True}
log_match={'logtype':1,'app_id':2,'match_id':132455,'contents':'HaiNQ test match log ffgfafd','response':True}

class Client(Protocol):
    def __init__(self,factory, number_request):
        self.buffer=deque()
        self.factory=factory

        
    def connectionMade(self):
        Protocol.connectionMade(self)
        self.d=self.request()
    
    def request(self):
        if self.factory.n<=0:
            #print 'decrem active client'
            self.factory.active-=1
            if self.factory.active==0:
                reactor.stop()  # @UndefinedVariable
            self.transport.loseConnection()       
            return None
        else:
            #print 'number request=',  self.factory.n
            self.factory.n-=1
            mess=Message(None,1,self.factory.id, log_user)
            data=mess.build_data()
            self.factory.id+=1
            self.transport.write(data)
            d=Deferred()
            d.addCallback(self.callback, time.time(), len(data))
            d.addErrback(self.errback)
            return d          
        
    def errback(self,failure):
        self.factory.fail_request+=1
        
    def callback(self, response_data,start_time ,send_size):
        #print 'callback'
        finish=time.time()
        latency=finish-start_time
        recv_size=len(response_data)
        #print latency, send_size, recv_size
        self.factory.add_statis(latency, send_size, recv_size)
        self.d=self.request()
       
    def dataReceived(self, data):
        Protocol.dataReceived(self, data)
        self.buffer.append(data)
        self.parseData()
        
    def parseData(self):
        #print 'parseData'
        data=''.join(self.buffer)
        self.buffer.clear()
        while True:
            try:
                length_data=len(data)
                print 'length_data', length_data
                if length_data > config.maximum_package_size:
                    self.buffer.append(data)
                    raise Exception("Bad request: size of package too large", length_data)
                if length_data < 4:
                    self.buffer.append(data)
                    return
                else:
                    length_payload,=struct.unpack("!I",data[0:4])
                    print 'length_payload', length_payload
                    if length_payload > config.maximum_package_size:
                        self.buffer.append(data)
                        raise Exception("Bad request: Payload length to large", length_payload)
                    length_package= 4 + length_payload
                    print 'length_package', length_package
                    if length_data < length_package:
                        #print 're append'
                        self.buffer.append(data)
                        return
                    else:
                        if self.d is not None:
                            self.d.callback(data[0:length_package])
                            payload=data[4:length_package]       
                            #print 'mess process'        
                            mess=Message(payload)
                            data=data[length_package:]    
                            if data:
                                self.buffer.append(data)  
#                         mess=Message(payload)
                        
            except:
                print traceback.format_exc()
                self.transport.loseConnection()
                return
        
class BenchmarkFactory(ClientFactory):
    def __init__(self, c=1, n=1):
        self.latency=[]
        self.send_size=[]
        self.recv_size=[]
        self.c=c
        self.n=n
        self.active=c
        self.fail_request=0
        self.id=0
    
    def buildProtocol(self, addr):
        return Client(self,int(self.n/self.c))
                      
    def add_statis(self,latency, send_size, recv_size):
        self.latency.append(latency)
        self.send_size.append(send_size)
        self.recv_size.append(recv_size)
        
        
    @staticmethod
    def process(data):
        pass
 
def check_stop_reactor(factory):
    #print 'factory.active', factory.active
    if factory.active<=0:
        reactor.stop()
    
    
if __name__=='__main__':
    print """"This is tool for benchmark TCP server 
writen in python by quochai.kstn@gmail.com"
User should inherit and override parseData method in Client class"""
    c=1 # concurency
    n=1 # number request
    print sys.argv
    for i in xrange(len(sys.argv)):
        if sys.argv[i]=='-h':
            try:
                h=(sys.argv[i+1])
            except:
                print traceback.format_exc()
                h=config.interface
        if sys.argv[i]=='-p':
            try:
                p=int(sys.argv[i+1])
            except:
                print traceback.format_exc()
                p=config.port
        if sys.argv[i]=='-c':
            try:
                c=int(sys.argv[i+1])
            except:
                print traceback.format_exc()
                c=1
        if sys.argv[i]=='-n':
            try:
                n=int(sys.argv[i+1])
            except:
                print traceback.format_exc()
                n=1
    start=time.time()
    print 'c=',c,'n=', n
    factory=BenchmarkFactory(c,n)   
    for i  in xrange(c):
        reactor.connectTCP(h, p, factory)   
    reactor.run()
    finish=time.time()
    #print n,factory.fail_request
    template = "{0:40}{1:10}{2:15}"
    data=[("Time for test:",'', finish-start)]
    data.append(("Concurency level",'',c))
    data.append(("Complete request",'',n))
    data.append(("fail request",'',factory.fail_request))
    data.append( ("Total transfer(byte)",'', sum(factory.send_size)))
    data.append(("Total receive(byte)",'', sum(factory.recv_size)))
    data.append( ( "Request per second",'', str((n-factory.fail_request)/(finish-start))+" #/second") )
    data.append(("Time per request",'',str(1000*(finish-start)/len(factory.latency))+" ms"))
    data.append(('transfer rate (from server)','',str(sum(factory.recv_size)/(1024*(finish-start))) +" kbyte/s" ) )
    for item in data:
        print template.format(*item)
    
    #print "len(latency)", len(factory.latency)
    