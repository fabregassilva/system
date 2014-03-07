"""
    @author: hainq@gviet.vn
    @since: Feb 2014
    @last update: Feb 2014
"""

from rpc_factory import RPC_Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
import config


class Server:
    def __init__(self):
        self.endpoint=TCP4ServerEndpoint(reactor, config.port, config.backlog,config.interface)
        self.endpoint.listen(RPC_Factory())
        
    def start(self):
        reactor.run()