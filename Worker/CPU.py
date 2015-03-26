from BaseAgentWorker import BaseAgentWorker
from BaseAgentWorker import BaseQGAAgentWorker


class LoadAvg(BaseQGAAgentWorker):

    __conn = None

    def update(self):
        self.Timestamp = self.time()

        self.Message = {'action': 'LoadAvg'}
        loadAvg = self.get_load_avg()

        if loadAvg is not None:
            self.Message['content'] = [ float(i) for i in loadAvg]

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




