from Cookie import SimpleCookie


from scapy.all import *
from scapy.layers.inet import TCP
import httplib
import StringIO

from tld import get_tld

from data.cookie import Cookie as CookieData


class Cookies(object):
    def __init__(self, listeners, filter_string="tcp port http", pcap=None, interface=None, default_expiry=None):
        self.filter_string = filter_string
        self.listeners = listeners
        self.pcap = pcap
        self.interface = interface
        self.default_expiry = default_expiry

    def sniff(self):
        sniffkw = {
            "prn": self.extract,
            "filter": self.filter_string
        }

        if self.pcap:
            sniffkw["offline"] = self.pcap
        elif self.interface:
            sniffkw["iface"] = self.interface

        sniff(**sniffkw)

    def extract(self, pkt):
        payload = str(pkt[TCP].payload)
        try:
            raw_headers = payload[payload.index(b"HTTP/"):payload.index(b"\r\n\r\n") + 2]
            unicode_data = unicode(raw_headers, "utf-8")
            raw_headers = StringIO.StringIO(unicode_data)

            http_headers = httplib.HTTPMessage(raw_headers, 0)
            http_headers.readheaders()

            cookie_type = None

            if http_headers.has_key(b"Cookie"):
                cookie_type = b"Cookie"
            elif http_headers.has_key(b"Set-Cookie"):
                cookie_type = b"Set-Cookie"

            if cookie_type:
                self.process_cookie(http_headers.get(cookie_type), http_headers.get(b"Host"))
        except Exception:
            pass

    def process_cookie(self, cookie, host):
        parsed = SimpleCookie(str(cookie))

        for key, c in parsed.items():
            if b"domain" in c:
                host = c['domain']

            url = self.create_url(host)
            host_tld = self.tld_parse(url)

            self.send_cookie_to_listeners(CookieData(name=c.key, value=c.value, domain="." + host_tld, url=url, expiry=self.default_expiry))

    def send_cookie_to_listeners(self, cookie):
        if self.listeners:
            for listener in self.listeners:
                listener.notify(cookie)

    @staticmethod
    def tld_parse(host):
        return get_tld(host)

    @staticmethod
    def create_url(host, schema=b"http", path="/"):
        host = host[1:] if host[0] == "." else host

        return b"{schema}://{host}/".format(schema=schema, host=host, path=path)
