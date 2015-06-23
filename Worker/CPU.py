from BaseAgentWorker import BaseAgentWorker
from BaseAgentWorker import BaseQGAAgentWorker


class LoadAvg(BaseQGAAgentWorker):

    __conn = None

    def update(self):
        self.Timestamp = self.time()

        self.Message = {'action': 'LoadAvg'}
        self.Message['content'] =""
        loadAvg = self.get_load_avg()

        if loadAvg is not None:
            msg = [ float(i) for i in loadAvg]
            if msg != self.Message['content']:
                self.Change = True
                self.Message['content'] = msg
            else:
                self.Change = false

        else:
            self.Priority = self.ERROR
            self.Message['content'] = "pipe broken!"

            self.exit()

    def get_load_avg(self):
        try:
            content = self.fetch('/proc/loadavg')

            content = content.split(" ")
            return content[:3]
        except:
            return None

    def analysis(self):
        pass




