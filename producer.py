import os
from Worker import *
from libs.Service import LongPollingService
from libs.Configuration import Configuration
from optparse import OptionParser
import gevent
import os.path
import time

parser = OptionParser()
parser.add_option("-d", "--fork", dest="fork",
                  help="Run in background", default=False, action="store_true")
parser.add_option("-f", "--conf",
                  dest="conf", default="etc/qga_agent.conf",
                  help="Configuration file")

(options, args) = parser.parse_args()

CFG = Configuration(options.conf)

def getAllQGA():
    socketPath = CFG.getOption("qga", "path")
    socket = set()

    for filename in os.listdir(socketPath):
        filename = os.path.join(socketPath , filename)
        #When vm starting, the QGA can't access normally. So wait 5min for QGA agent launched.
        if os.path.getmtime(filename) > time.time() - 300: continue
        #exclude some files which not qga sockets
        if filename[-4:] != 'sock': continue

        socket.add(filename)

    return socket

def buildWorker(indication, hostname, filename):
    obj =  eval(indication)
    return obj(hostname,filename)

def getLogger():
    type = CFG.getOption("qga", "logger")
    cls = "from Dispatcher.%s import Collection" % type
    exec (cls)

    handle = Collection(CFG.getSection(type))
    return handle

def setJob(service, hostname, files):
    for filename in files:
        for indication in CFG.getOption("qga", "indexes").split(","):
            if (len(indication) == 0) : continue
            worker = buildWorker(indication, hostname, filename)
            service.add(worker)

def main():
    fetch_interval = float(CFG.getOption("qga", "fetch_interval"))
    hostname = CFG.getOption("qga", "hostname")

    service = LongPollingService(fetch_interval)

    loggerHandle = getLogger()

    service.setLogger(loggerHandle)
    fileList = orignal = getAllQGA()
    setJob(service, hostname, fileList)

    service.start()
    checkSockeInterval = int(CFG.getOption('qga', 'check_socket_interval'))

    while True:
        #new sockets checker, if added 1 newer, push to Q
        gevent.sleep(checkSockeInterval)
        fileList = getAllQGA()
        if fileList != orignal:
            setJob(service, hostname, fileList - orignal)
            orignal = fileList

    service.join()

if __name__ == '__main__':
    main()