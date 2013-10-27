'''
Supernode Parameters

Usage: supernode -v -v -f -l <port> -i <ip>:<port>
'''

from cmn.param import Param
from cmn.n2n_params import N2NParams
    

class SupernodeParams(N2NParams):
    
    def __init__(self):
        N2NParams.__init__(self)
        self.port       = Param(Param.STR, "l")
        self.mgmt_port  = Param(Param.STR, "t")
        self.supernode  = Param(Param.STR, "i")

