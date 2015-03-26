import socket
import json
import commands
import re

class _QGAInterface(object):

    def __init__(self, filename): pass

    def send(self, command): pass

    def recieve(self): pass

    def close(self): pass


class QGASocket(_QGAInterface):
    handler = None

    def __init__(self, filename):
        if self.handler is None:
            self.connect(filename)

    def __del__(self):
        if self.handler is not None:
            self.close()

    def close(self):
        self.handler.close()

    def connect(self, filename):
        address = filename
        self.handler = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.handler.settimeout(1)

        self.handler.connect(address)

    def recieve(self):
        result = self.handler.recieve(1024)
        return json.loads(result)

    def send(self, command):
        self.handler.send(json.dumps(command))


class QGACommandLine(_QGAInterface):

    domain = None
    virsh = "/usr/bin/virsh qemu-agent-command --domain %s '%s'"
    command = None

    def __init__(self, filename):
        # Normal format: org.qemu.guest_agent.0.instance-0000002c.sock
        #if the format has been changed, change it here!
        reg = r'org\.qemu\.guest_agent\.\w{1}\.(instance-\w{8})\.sock'
        self.domain = re.search(reg, filename).group(1)

    def send(self, command):
        self.command = self.virsh % (self.domain, json.dumps(command))

    def recieve(self):
        if self.command is None:
            return None
        (status, output) = commands.getstatusoutput(self.command)
        if status != 0:
            raise IOError
        return json.loads(output)
