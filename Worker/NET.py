from BaseAgentWorker import BaseQGAAgentWorker
import re
import commands

reg = r'\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}'

class IPAddr(BaseQGAAgentWorker):

    __conn = None
    count = 0
    msg = ''

    def update(self):
        self.Timestamp = self.time()

        self.Message = {'action': 'NetWork'}
        self.Message['content'] = ''
        NetInfo = self.get_net_info()
        ip = []
        ip_reg = re.compile(reg)
        if NetInfo is not None:
            if len(NetInfo["return"]) >1 :
                for Net in NetInfo["return"]:
                    ip.append(Net["ip-addresses"][0]["ip-address"])
                if self.msg == ip:
                    self.Change = False
                    self.count= self.count+1
                    # same in 5 times, send heartbeat
                    if self.count == 5:
                        self.Change = True
                        self.count = 0
                else:
                    self.Change = True
                    self.count = 0
                    self.Message['content'] = ip
                    self.msg = self.Message['content']
                for ip_addr in ip:
                    bool= ip_reg.match(ip_addr)
                    if not bool:
                        self.Priority=40

            else:
                return None

        else:
            self.Priority = self.ERROR
            self.Message['content'] = "pipe broken!"

            self.exit()

    def get_net_info(self):
        try:
            query = {'execute': 'guest-network-get-interfaces'}
            content = self.query(query)
            return content
        except:
            return None

    # if the data is not ok, check ovs status
    def analysis(self):
        nics = ['br-int', 'br-eth2','eth2']
        for nic in nics:
            command = 'ethtool '+ nic
            (status, output) = commands.getstatusoutput(command)
            # means nic is down
            if output == 'no':
                (status,output) = commands.getstatusoutput('ifconfig '+nic+' up')


