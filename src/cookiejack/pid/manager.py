import os
import signal


class Manager(object):
    def __init__(self, pid_file):
        self.pid_file = pid_file

    def update(self):
        with open(self.pid_file, "w") as f:
            f.write(str(os.getpid()))

    def kill(self):
        with open(self.pid_file) as f:
            os.kill(int(f.read()), signal.SIGHUP)
