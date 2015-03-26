from BaseAgentWorker import BaseQGAAgentWorker

class IPAddr(BaseQGAAgentWorker):

    __conn = None

    def update(self):
        self.Timestamp = self.time()

        self.Message = {'action': 'NetWork'}
        NetInfo = self.get_net_info()
        ip = []
        if NetInfo is not None:
            if len(NetInfo["return"]) >1 :
                for Net in NetInfo["return"]:
                    ip.append(Net["ip-addresses"][0]["ip-address"])
                self.Message['content'] = ip
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
