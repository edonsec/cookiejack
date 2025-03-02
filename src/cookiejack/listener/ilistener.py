import zope.interface.interface


class IListener(zope.interface.Interface):
    def notify(cookie):
        """Receive a cookie from the sniffer"""
