"""
    @author: hainq@gviet.vn
    @since: Feb 2014
    @last update: Feb 2014
"""

from twisted.internet.protocol import ServerFactory
from rpc_protocol import RPC
from server_service import config

class RPC_Factory(ServerFactory):
    
    def __init__(self):
        self.number_connection=0
       
    def buildProtocol(self, addr):
        return RPC(self)
    
    def startFactory(self):
        ServerFactory.startFactory(self)
        print "log: server start"
