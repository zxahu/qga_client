from optparse import OptionParser
from libs.Configuration import Configuration
parser = OptionParser()
parser.add_option("-f", "--conf",
                  dest="conf", default="etc/qga_agent.conf",
                  help="Configuration file")
(options, args) = parser.parse_args()

CFG = Configuration(options.conf)

class BaseDispatcher(object):


    def __init__(self, cfg):
        pass

    def __del__(self):
        pass

    def save(self, agentWorker):
        pass

