import argparse
from Queue import Queue
from threading import Thread
import sys
from pid.manager import Manager
from listener.queuer import Queuer as WebsocketNotifier
from listener.printer import Printer as PrinterNotifier
from server.injector_protocol import InjectorProtocol
from server.websocket import WebSocket
from sniff.cookies import Cookies as CookieSniffer
from validator import cookie_date


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ws-port", "-p", help="Port to bind websocket server on", default=9000, type=int)
    parser.add_argument("--ws-bind", "-wi", help="Interface to bind websocket server on", default="127.0.0.1")
    parser.add_argument("--sniff", "-s", help="Sniffing filter string", default="tcp port 80")
    parser.add_argument("--pcap", "-r", help="PCAP file to load", default=None)
    parser.add_argument("--interface", "-i", help="Network interface to sniff on", default=None)
    parser.add_argument("--verbose", "-v", help="Display cookie data", action="store_true")
    parser.add_argument("--pid-log", "-l", help="File where process id will be written",
                        default="/tmp/cookiejack.pid")
    parser.add_argument("--kill", "-k", help="Kill the application", action="store_true")
    parser.add_argument("--cookie-expiry", "-e", help="Default cookie expiry", default=None, type=cookie_date)

    args = parser.parse_args()

    q = Queue()
    listeners = [WebsocketNotifier(q)]
    pid_manager = Manager(args.pid_log)

    if args.kill:
        pid_manager.kill()
        sys.exit(0)

    pid_manager.update()

    if args.verbose:
        listeners.append(PrinterNotifier())

    cookie_sniffer = CookieSniffer(listeners, filter_string=args.sniff, interface=args.interface, pcap=args.pcap, default_expiry=args.cookie_expiry)
    p = Thread(target=cookie_sniffer.sniff)
    p.start()

    server = WebSocket(args.ws_port, InjectorProtocol, bind=args.ws_bind)
    server.run(q)
