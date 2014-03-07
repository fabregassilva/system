"""
    @author: hainq@gviet.vn
    @since: Feb 2014
    @last update: Feb 2014
"""

import msgpack
from collections import deque
import struct
import traceback


class Message:
    
    def __init__(self, payload=None,type_=None,id_=None,data=None):
        """
            payload: raw payload data from network
        """
        if payload:
            try:
                self.type,=struct.unpack("!H",payload[0:2])
                #print 'type',self.type
                self.id,=struct.unpack("!I",payload[2:6])
                #print 'id', self.id
                #print len(payload[6:])
                self.data=msgpack.unpackb(payload[6:])  
                #print 'data', self.data
                 
            except Exception,e:
                raise Exception("payload don't have correct structure",e)
        else:
            self.type=type_
            self.id=id_
            self.data=data
    
    def set_type(self,type_package):
        
        self.type=type_package
    def get_type(self):
        return self.type
    
    def set_id(self,identity):
        self.id=identity
    def get_id(self):
        return self.id
    
    def set_data(self,data):
        """
            data is python dictionary
        """
        self.data=data
        
    def get_data(self):
        return self.data
    
    def build_data(self):
        if self.data is not None:
            temp=struct.pack('!H',self.type)+struct.pack('!I',self.id)+msgpack.packb(self.data)
        else:
            temp=struct.pack('!H',self.type)+struct.pack('!I',self.id)
        return struct.pack("!I",len(temp))+temp