from twisted.internet.protocol import ClientFactory, Protocol, Factory
from twisted.internet import reactor
from twisted.internet.stdio import StandardIO
from twisted.conch.telnet import TelnetProtocol
from sys import stdout
from copy import copy

# This file creates a telnet proxy, connecting to achaea.com.
# The file works like this:
#
# Local client --> TelnetServer() --> TelnetClient() --> Achaea

class TelnetClient( TelnetProtocol):
        """
        TelnetClient() connects directly to the Achaea server.
        """
        
        myServer = None
        
        def dataReceived( self, data):
                """
                If you want to add triggers, they would go here.
                """
                
                self.myServer.transport.write( data)


class TelnetClientFactory( ClientFactory):
        """
        TelnetClientFactory() is magic. Do not edit.
        """

        myClient = TelnetClient()
        
        def startedConnected( self, connector):
                print "Started to connect."
        
        def buildProtocol( self, addr):
                print "Connected."
                return self.myClient
        
        def clientConnectionLost( self, connector, reason):
                print "Lost connection. Reason:", reason
                exit()
        
        def clientConnectionFailed( self, connector, reason):
                print "Connection failed. Reason:", reason

class TelnetServer( Protocol):
        """
        Local client connects to TelnetServer().
        TelnetServer() connects to TelnetClient()
        """

        myClient = None
        
        def connectionMade( self):
                """
                Local client connected. Start client connection to server.
                """

                self.transport.write( "Connected to PyMuddy")
                serverReactor = copy( reactor)
                telnetClientFactory = TelnetClientFactory()
                self.myClient = telnetClientFactory.myClient
                self.myClient.myServer = self
                
                # To use VadiSystem, change "achaea.com" to "localhost"
                # and 23 to 1234.
                serverReactor.connectTCP( "achaea.com", 23, telnetClientFactory)
                serverReactor.run()
        
        def dataReceived( self, data):
                """
                Input received; forward data to myClient's transport.
                
                Further, if you would like to add aliases, the code
                should go here.
                """

                self.myClient.transport.write( data)

def main():
        factory = Factory()
        factory.protocol = TelnetServer
        reactor.listenTCP( 10000, factory)
        reactor.run()

main()
