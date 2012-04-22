from twisted.internet.protocol import Factory, Protocol, ClientFactory
from twisted.internet import reactor
from twisted.conch.telnet import TelnetProtocol

class AchaeaClient(TelnetProtocol):
    
    def dataReceived(self, data):
        print data

class AchaeaClientFactory(ClientFactory):

    protocol = None

    def buildProtocol(self, addr):
        print("Connected to the Server")
        protocol = AchaeaClient()
        return protocol

def cat_main():
    achaea_client_factory = AchaeaClientFactory()
    reactor.connectTCP("achaea.com", 23, achaea_client_factory)
    reactor.run()

if __name__ == "__main__":
    cat_main()
