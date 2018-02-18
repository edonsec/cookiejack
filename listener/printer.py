import zope

from listener.ilistener import IListener


class Printer(object):
    zope.interface.implements(IListener)

    def __init__(self):
        pass

    def notify(self, cookie):
        print cookie.to_json()