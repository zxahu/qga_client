from BaseDispatcher import BaseDispatcher


class Collection(BaseDispatcher):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if (cls.__instance is None):
            cls.__instance = super(Collection, cls).__new__(cls, *args, **kwargs)

        return cls.__instance

    def save(self, agentWorker):

        content = {
            "timestamp": agentWorker.Timestamp,
            "host" : agentWorker.Host,
            "guest" : agentWorker.Guest,
            "priority" : agentWorker.Priority,
            "message"  : agentWorker.Message
                    }
        if agentWorker.Priority > agentWorker.INFO:
            print '\033[31m' + str(content) + '\033[0m'
        else:
            print content
