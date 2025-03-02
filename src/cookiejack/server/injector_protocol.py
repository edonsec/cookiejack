from autobahn.twisted import WebSocketServerProtocol
import queue


class InjectorProtocol(WebSocketServerProtocol):
    def __init__(self, queue, reactor):
        super(InjectorProtocol, self).__init__()

        self.queue = queue
        self.reactor = reactor

    def onConnect(self, request):
        print("Client connecting: {}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

        self.send_queued_items()

    def onMessage(self, payload, is_binary):
        pass

    def onClose(self, was_clean, code, reason):
        print("WebSocket connection closed: {}".format(reason))

    def send_queued_items(self):
        try:
            while not self.queue.empty():
                payload = self.queue.get_nowait()
                print("Queue item being sent.")
                self.sendMessage(payload.encode())
        except queue.Empty:
            pass
        finally:
            self.reactor.callLater(5, self.send_queued_items)

    def _handle_send_error(self, failure):
        print(f"Error sending message: {failure.getErrorMessage()}")
        self.queue.put(failure.value)
