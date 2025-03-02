from twisted.internet import reactor
from .injector_factory import InjectorFactory
import os, pwd, grp


class WebSocket(object):
    def __init__(self, port, protocol_factory, bind="127.0.0.1"):
        self.port = port
        self.protocol_factory = protocol_factory
        self.bind = bind

    def run(self, queue):
        #self.drop_privileges()
        factory = InjectorFactory(queue, reactor)

        print(f"Listening on port {self.port}")
        reactor.listenTCP(self.port, factory, interface=self.bind)
        reactor.run()

    @staticmethod
    def drop_privileges(uid_name='nobody', gid_name='nogroup'):
        if os.getuid() != 0:
            return

        running_uid = pwd.getpwnam(uid_name).pw_uid
        running_gid = grp.getgrnam(gid_name).gr_gid

        os.setgroups([])

        os.setgid(running_gid)
        os.setuid(running_uid)
        os.umask(0o770)
