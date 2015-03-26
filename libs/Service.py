import gevent
from gevent import Greenlet


class LongPollingService(Greenlet):

    InstancePool = []
    InterVal = 5

    LoggerHandle = None

    def __init__(self, interval = 5):
        Greenlet.__init__(self)
        self.InterVal = interval

    def _run(self):
        while True:

            for agentWorker in self.InstancePool:
                # update
                agentWorker.update()
                #save log
                self.log(agentWorker)

                # remove from list, if exit signal enabled
                if agentWorker.Exit:
                    self.InstancePool.remove(agentWorker)
                    del(agentWorker)

                gevent.sleep(0)
            gevent.sleep(self.InterVal)

    def add(self, instance):
        self.InstancePool.append(instance)

    def log(self, agentWorker):
        self.Logger.save(agentWorker)

    def setLogger(self, handle):
        self.Logger = handle
