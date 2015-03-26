from BaseAgentWorker import BaseAgentWorker
from BaseAgentWorker import BaseQGAAgentWorker
from libs.MatrixFilter import ColumnMatrixFilter


class Free(BaseQGAAgentWorker):

    __conn = None
    matrixFilter = {}

    def __init__(self, host, filename=None):
        super(Free, self).__init__(host, filename)
        self.initialFilter()

    def initialFilter(self):
        self.matrixFilter['MemTotal'] = ColumnMatrixFilter('MemTotal:')
        self.matrixFilter['MemFree'] = ColumnMatrixFilter('MemFree:')

    def update(self):
        self.Timestamp = self.time()

        self.Message = {'action': 'MemStatus'}

        meminfo = self.getMemInfo()
        status = self.getStatus(meminfo)

        if status is not None:
            self.Message['content'] = status
            if status['rate'] > 0.9:
                self.Priority = self.ERROR
                status['message'] = "RAM usage too hight"
        else:
            self.Priority = self.ERROR
            self.Message['content'] = "pipe broken!"

            self.exit()

    def getMemInfo(self):
        try:
            return self.fetch('/proc/meminfo')
        except:
            return None

    def getStatus(self, content):
        try:
            memtotal = int(self.matrixFilter['MemTotal'].do(content))
            memfree  = int(self.matrixFilter['MemFree'].do(content))
            memrate  = 1 - float(memfree) / memtotal

            result =  {"total": memtotal, 'free': memfree, 'rate' : memrate }
            return result

        except:
            return  {"total": 0, 'free': 0, 'rate' : 0 }

class Swap(BaseQGAAgentWorker):

    __conn = None
    matrixFilter = {}

    def __init__(self, host, filename=None):
        super(Swap, self).__init__(host, filename)
        self.initialFilter()

    def initialFilter(self):
        self.matrixFilter['SwapTotal'] = ColumnMatrixFilter('SwapTotal:')
        self.matrixFilter['SwapFree'] = ColumnMatrixFilter('SwapFree:')

    def update(self):
        self.Timestamp = self.time()

        self.Message = {'action': 'SwapStatus'}

        meminfo = self.getMemInfo()
        status = self.getStatus(meminfo)

        if status is not None:
            self.Message['content'] = status

            if status['rate'] > 0.9:
                self.Priority = self.ERROR
                status['message'] = "Swap usage too hight"
        else:
            self.Priority = self.ERROR
            self.Message['content'] = "pipe broken!"

            self.exit()

    def getMemInfo(self):
        try:
            return self.fetch('/proc/meminfo')
        except:
            return None

    def getStatus(self, content):
        try:

            swaptotal = int(self.matrixFilter['SwapTotal'].do(content))
            swapfree  = int(self.matrixFilter['SwapFree'].do(content))

            if swaptotal == 0:
                swaprate = 0
            else :
                swaprate  = 1 - float(swapfree) / swaptotal

            result =  {"total": swaptotal, 'free': swapfree, 'rate' : swaprate }
            return result

        except:
            return  {"total": 0, 'free': 0, 'rate' : 0 }
