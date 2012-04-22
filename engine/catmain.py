from twisted.internet.protocol import Factory, Protocol, ClientFactory
from twisted.internet import reactor
from twisted.conch.telnet import TelnetProtocol

class AchaeaClient(TelnetProtocol):
    
    server_ref = None

    def dataReceived(self, data):
        self.server_ref.transport.write(data)

class AchaeaClientFactory(ClientFactory):

    client_ref = AchaeaClient()

    def startedConnected(self, connector):
        print("Starting to connect.")
        
    def buildProtocol(self, addr):
        print("Connected to the Server")
        return self.client_ref

    def clientConnectionLost(self, connector, reason):
        if "Connection was closed cleanly." not in str(reason):
            print("Lost connection due to: %s." % reason)
        else:
            print("Connection ended gracefully")
        self.client_ref.server_ref.close_connection()
        
    def clientConnectionFailed(self, connector, reason):
        print("Connection failed due to: %s." % reason)

class CatmainProtocol(Protocol):
    
    client_ref = None
    
    def connectionMade(self):
        self.transport.write("Connected to Catmain")
        achaea_client_factory = AchaeaClientFactory()
        self.client_ref = achaea_client_factory.client_ref
        self.client_ref.server_ref = self
        
        reactor.connectTCP("achaea.com", 23, achaea_client_factory)
        
    def dataReceived(self, data):
        self.client_ref.transport.write(data)

    def close_connection(self):
        print("Closing connection to client.")
        self.transport.loseConnection()
        reactor.stop()

def cat_main():
    factory = Factory()
    factory.protocol = CatmainProtocol
    reactor.listenTCP(10000, factory)
    reactor.run()

if __name__ == "__main__":
    cat_main()
