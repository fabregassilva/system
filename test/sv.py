from twisted.internet.protocol import Protocol

class Echo(Protocol):

    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.factory.numProtocols = self.factory.numProtocols+1 
        self.transport.write(
            "Welcome! There are currently %d open connections.\n" %
            (self.factory.numProtocols,))

    def connectionLost(self, reason='kj'):
        print 'lose connection'
        self.factory.numProtocols = self.factory.numProtocols-1

    def dataReceived(self, data):
        self.transport.write(data)
        

from twisted.internet.protocol import Protocol

class QOTD(Protocol):

    def connectionMade(self):
        print 'connectionMade'
        self.transport.write("An apple a day keeps the doctor away\r\n") 
        self.transport.loseConnection()
        
    def connectionLost(self, reason):
        Protocol.connectionLost(self, reason)
        print 'lose connection'

from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor

class QOTDFactory(Factory):
    def buildProtocol(self, addr):
        return QOTD()

# 8007 is the port you want to run under. Choose something >1024
endpoint = TCP4ServerEndpoint(reactor, 8007)
endpoint.listen(QOTDFactory())
reactor.run()