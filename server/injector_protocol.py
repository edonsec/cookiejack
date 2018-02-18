from autobahn.twisted import WebSocketServerProtocol


class InjectorProtocol(WebSocketServerProtocol):
    def __init__(self, queue, reactor):
        super(InjectorProtocol, self).__init__()

        self.queue = queue
        self.reactor = reactor

    def onConnect(self, request):
        print("Client connecting: {}".format(request.peer))

    def onOpen(self):
        print "WebSocket connection open."

        self.send_queued_items()

    def onMessage(self, payload, is_binary):
        pass

    def onClose(self, was_clean, code, reason):
        print("WebSocket connection closed: {}".format(reason))

    def send_queued_items(self):
        for i in range(0, self.queue.qsize()):
            payload = self.queue.get(False)

            print "Sending queue item"
            self.sendMessage(payload)

        self.reactor.callLater(5, self.send_queued_items)
