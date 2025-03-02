from zope.interface import implementer
from .ilistener import IListener


@implementer(IListener)
class Printer(object):
    def __init__(self):
        pass

    def notify(self, cookie):
        print(cookie.to_json())
