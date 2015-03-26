from BaseAgentWorker import BaseAgentWorker
'''
You may write some fake indexes here for testing
'''


class counter(BaseAgentWorker):
    #Host = None
    counter = 0
    # def __init__(self, filename):
    #     self.Host = filename
    __Content = None

    def update(self):
        self.Priority = self.INFO

        self.Timestamp = self.time()
        self.counter +=1

        self.Message = {'counter' : self.counter}

        if self.counter & 1 == 0 :
            self.Priority = self.ERROR
            self.Message['error'] = "ODD"

        if self.counter > 15:
            self.exit()


class performance(BaseAgentWorker):

    last = 0

    def update(self):
        self.Priority = self.INFO
        self.Timestamp = self.time()

        self.last += 1
        if self.last > 35 :
            self.exit()
            self.Priority = self.ERROR
            self.Message = {"result" : 0}
        else:
            self.Message = {"result" : self.slow(self.last)}

    def slow(self, i):
        if i < 2 : return 1
        if i < 5 : return self.slow(i-1) + self.slow(i-2)
        return self.slow(i-1) + self.slow(i-2) - self.slow(i-5)