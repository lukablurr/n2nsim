'''
Simulated client
'''

from cmn.nodesim import NodeSim
from client.clientcfg import ClientConfig
from client.edge import Edge
from client.app import App


class ClientSim(NodeSim):
    
    CONFIG = ClientConfig()
    
    def __init__(self, ip, port, mport):
        NodeSim.__init__(self, ip, port, mport)
        self.edge = Edge()
        '''
                edge.params.super_addr.setValue(super_addr)#TODO
                edge.params.device_name.setValue("n2n%02d" % (i * j))
                edge.params.device_mac.setValue("3C:A0:12:34:56:78")#TODO
                edge.params.device_addr.setValue("1.2.3.4")#TODO
        '''
        
        self.app = App()
    
    def start(self):
        self.addAddress()
        self.edge.params.port.setValue( self.localAddress() )
        self.edge.run(ClientSim.CONFIG.path)
    
    def stop(self):
        self.edge.stop()
        self.deleteAddress()

