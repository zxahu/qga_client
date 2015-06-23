from BaseDispatcher import BaseDispatcher
import pika
import json
import logging
import logging.handlers

class Collection(BaseDispatcher):
    __instance = None

    Host = 'localhost'
    Queue = 'database'
    log_path = '/var/log/qga_error.log'
    log_format = '%(asctime)s - %(filename)s:%(lineno)s - %(levelname)s - %(message)s'
    connection = None
    channel = None

    def __new__(cls, *args, **kwargs):
        if (cls.__instance is None):
            cls.__instance = super(Collection, cls).__new__(cls, *args, **kwargs)

        return cls.__instance

    def __init__(self, cfg):
        keys = cfg.keys()
        if 'host' in keys:
            self.Host = cfg['host']
        if 'log_path' in keys:
            self.log_path = cfg['log_path']
        self.init_log()
        self.connect()

    def __del__(self):
        if self.connection is not None:
            self.connection.close()   

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=self.Host))
            self.channel = self.connection.channel()
        except :
            self.logger.error("connect to rabbitmq-server failed  ")
            raise Exception("connect to rabbitmq-server failed ")

    def init_log(self):
        LOG_FILE = self.log_path
        handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes = 1024*1024, backupCount = 5)   
        formatter = logging.Formatter(self.log_format)  
        handler.setFormatter(formatter)  
        self.logger = logging.getLogger(LOG_FILE)
        self.logger.addHandler(handler)         
        self.logger.setLevel(logging.DEBUG)
        
    def save(self, agentWorker):
        if agentWorker.Change == True:
            content = {
                "timestamp": agentWorker.Timestamp,
                "host" : agentWorker.Host,
                "guest" : agentWorker.Guest,
                "priority" : agentWorker.Priority,
                "message"  : agentWorker.Message,
                "uuid": agentWorker.uuid,
                "image":agentWorker.image
            }

            qga_message = json.dumps(content)
            try:
                self.channel.basic_publish(exchange='',
                    routing_key=self.Queue,
                    body=qga_message,
            properties=pika.BasicProperties(delivery_mode = 2,))
            except :
                self.logger.error("send message to rabbitmq-server failed  "+ qga_message)

