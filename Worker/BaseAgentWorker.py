import time
import os
import base64
#from libs.QGASocket import QGASocket as QGA
from libs.QGASocket import QGACommandLine as QGA


class BaseAgentWorker(object):

    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10

    Host = "localhost"
    Guest = None
    Name = ''
    Priority = 20
    Message = {}
    Timestamp = 0

    Connection = None
    #the exit signals
    Exit = False

    def __init__(self, host, filename=None):
        self.Host = host
        self.Guest = os.path.split(filename)[-1]
        self.Name = self.__class__.__name__

    def __del__(self):
        pass

    def update(self):
        self.Timestamp = self.time()

    def time(self):
        return time.time()

    def exit(self):
        self.Exit = True


class BaseQGAAgentWorker(BaseAgentWorker):
    __conn = None
    socketFile = None
    _die_time = 0

    def __init__(self, host, filename=None):
        self.Host = host
        self.Guest = os.path.split(filename)[-1]

        self.socketFile = filename
        self.connect()

    def __del__(self):
        if self.__conn is not None:
            self.__conn.close()

    def connect(self):
        try:
            if self.__conn is None:
                self.__conn = QGA(self.socketFile)
        except:
            self.Priority = self.ERROR
            self.Message  = {'message': "can't connection to qga"}

            self.exit()

    def fetch(self, filename):
        self.connect()

        query = {'execute': 'guest-file-open', 'arguments': {'path': filename, 'mode': 'r'}}
        result = self.query(query)

        if 'return' not in result.keys() or result['return'] < 0:
            return None

        fileHandleId = result['return']

        data = ''
        query= {'execute': 'guest-file-read', 'arguments': {'handle': fileHandleId, 'count': 1 << 11}}
        while True:
            try:
                self.__conn.send(query)
                result = self.__conn.recieve()
                data += result['return']['buf-b64']

                if result['return']['eof']:
                    break
            except:
                self.exit()
                return None

        #close file handle
        query = {'execute': 'guest-file-close', 'arguments': {'handle': fileHandleId}}
        self.query(query)

        return base64.decodestring(data)

    def query(self, command):
        try:
            self.__conn.send(command)
            return self.__conn.recieve()
        except:
            self.exit()
            return None

    def exit(self):

        if self._die_time < 3:
            self.Exit = True

        else:
            try:
                command = {'execute' : 'guest-ping'}
                self.query(command)
                self._die_time = 0
            except:
                self._die_time += 1
