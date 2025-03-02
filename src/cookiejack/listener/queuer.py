import zope as zope

from zope.interface import implementer
from cookiejack.listener.ilistener import IListener


@implementer(IListener)
class Queuer(object):
    def __init__(self, queue):
        self.queue = queue

    def notify(self, cookie):
        print("Socket notified")
        self.queue.put(cookie.to_json())
