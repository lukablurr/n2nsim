'''
Supernode Parameters

Usage: supernode -v -v -f -l <port> -i <ip>:<port>
'''

from cmn.param import Param
from cmn.n2n_params import N2NParams
    

class SupernodeParams(N2NParams):
    
    def __init__(self):
        N2NParams.__init__(self)
        self.port       = Param(Param.INT, "l")
        self.mgmt_port  = Param(Param.INT, "t")
        self.supernode  = Param(Param.STR, "i")

