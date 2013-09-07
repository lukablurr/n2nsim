'''
Supernode wrapper
'''

from cmn.n2n_process import N2NProcess
from server.supernodep import SupernodeParams


class Supernode(N2NProcess):
    
    PATH = "supernode"
    
    def __init__(self, ip_str):
        N2NProcess.__init__(self)
        self.params = SupernodeParams()
        self.params.foreground.setValue(True)


