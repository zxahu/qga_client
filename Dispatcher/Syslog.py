from BaseDispatcher import BaseDispatcher
import logging
from logging.handlers import SysLogHandler
import json


class Collection(BaseDispatcher):

    Format = '%(message)s'
    Handle = None

    Host = 'localhost',
    Port = 514
    Facility = 'local0'

    __instance = None


    def __new__(cls, *args, **kwargs):
        if (cls.__instance is None):
            cls.__instance = super(Collection, cls).__new__(cls, *args, **kwargs)

        return cls.__instance

    def __init__(self, cfg):
        keys = cfg.keys()
        if 'host' in keys:
            self.Host = cfg['host']

        if 'port' in keys:
            self.Port = int(cfg['port'])

        if 'facility' in keys:
            self.Facility = cfg['facility']

        handler = SysLogHandler(address=(self.Host, self.Port), facility=self.Facility)

        if 'format' in keys:
            self.Format = cfg['format']

        format = logging.Formatter(self.Format)
        handler.setFormatter(format)

        logger = logging.getLogger()
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    def save(self, agentWorker):
        content = {
            "host" : agentWorker.Host,
            "guest" : agentWorker.Guest,
            "message"  : agentWorker.Message
                    }

        logging.log(agentWorker.Priority, json.dumps(content))
