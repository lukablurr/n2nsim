'''
Simulated server
'''

from cmn.nodesim import NodeSim
from server.servercfg import ServerConfig
from server.supernode import Supernode
from utils.net import int2ip


class ServerSim(NodeSim):
    
    CONFIG = ServerConfig()
    
    def __init__(self, ip, port, mport, super_addr=None):
        NodeSim.__init__(self, ip, port, mport)
        self.supernode = Supernode("")
        if super_addr:
            ip, port = super_addr
            addr = "%s:%d" % (int2ip(ip), port)
            self.supernode.params.supernode.setValue(addr)
    
    def start(self):
        self.addAddress()
        self.supernode.params.port.setValue( self.localAddress() )
        self.supernode.params.mgmt_port.setValue( self.mgmtAddress() )
        self.supernode.run(ServerSim.CONFIG.path)
    
    def stop(self):
        self.supernode.stop()
        self.deleteAddress()

