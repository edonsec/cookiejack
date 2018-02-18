from autobahn.twisted import WebSocketServerFactory

from server.injector_protocol import InjectorProtocol


class InjectorFactory(WebSocketServerFactory):
    protocol = InjectorProtocol

    def __init__(self, queue, reactor, *args, **kwargs):
        super(InjectorFactory, self).__init__(*args, **kwargs)

        self.queue = queue
        self.reactor = reactor

    def buildProtocol(self, *args, **kwargs):
        protocol = InjectorProtocol(self.queue, self.reactor)
        protocol.factory = self

        return protocol
