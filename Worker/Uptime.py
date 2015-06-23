__author__ = 'zhang11'

from BaseAgentWorker import BaseAgentWorker
from BaseAgentWorker import BaseQGAAgentWorker


class Uptime(BaseQGAAgentWorker):

    __conn = None

    def update(self):
        self.Timestamp = self.time()

        self.Message = {'action': 'uptime'}
        self.Message['content'] =""
        Uptime = self.get_uptime()

        if Uptime is not None:
            msg = [ float(i) for i in Uptime]
            self.Message['content'] = msg
        else:
            self.Priority = self.ERROR
            self.Message['content'] = "pipe broken!"

            self.exit()

    def get_uptime(self):
        try:
            content = self.fetch('/proc/uptime')

            content = content.split(" ")
            return content[:1]
        except:
            return None

    def analysis(self):
        pass