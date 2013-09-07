'''
Edge wrapper
'''

import socket
from cmn.n2n_process import N2NProcess
from client.edgep import EdgeParams
from client import n2n_community


class Edge(N2NProcess):
    
    PATH = "edge"
    
    def __init__(self):
        N2NProcess.__init__(self)
        self.params = EdgeParams()
        self.params.foreground.setValue(True)
        print (self.params.mgmt_port.value)
            
    def setCommunity(self, n2n_community):
        if not n2n_community:
            self.params.community.disable()
            self.params.key.disable()
            return
        
        self.params.community.setValue(n2n_community.name)
        if n2n_community.key:
            self.params.key.setValue(n2n_community.key)
        
    def stop(self): # overridden
        if not self.process:
            return
        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        addr = ("127.0.0.1", self.params.mgmt_port.value)
        sock.sendto("stop", addr)
        self.process.wait()

'''
call(["ip", "addr", "add", server_ip, "dev", dev_name])
'''