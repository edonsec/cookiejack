import zope as zope

from listener.ilistener import IListener


class Queuer(object):
    zope.interface.implements(IListener)

    def __init__(self, queue):
        self.queue = queue

    def notify(self, cookie):
        self.queue.put(cookie.to_json())
