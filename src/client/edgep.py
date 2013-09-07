'''
Edge Parameters

Usage: edge -f -d n2n0 -c mynetwork -k encryptme -u 99 -g 99 -m 3C:A0:12:34:56:78 -a dhcp:1.2.3.4 -l 192.168.1.102:7777
'''

from cmn.param import Param
from cmn.n2n_params import N2NParams


class EdgeParams(N2NParams):
    
    def __init__(self):
        N2NParams.__init__(self)
        
        self.community  = Param(Param.STR,  "c")
        self.port       = Param(Param.INT,  "p")
        self.mgmt_port  = Param(Param.INT,  "t", 5644)
        self.routing    = Param(Param.BOOL, "r")

        self.super_addr         = Param(Param.STR,  "l")
        self.resolve_super_ip   = Param(Param.BOOL, "b")

        self.device_name = Param(Param.STR, "d")
        self.device_addr = Param(Param.STR, "a")
        self.device_mask = Param(Param.STR, "s")
        self.device_mac  = Param(Param.STR, "m")
        self.device_mtu  = Param(Param.INT, "M")
        self.accept_multicast = Param(Param.BOOL, "E")
        
        self.key        = Param(Param.STR, "k")
        self.key_file   = Param(Param.STR, "K")
        
        self.uid        = Param(Param.INT,  "u")
        self.gid        = Param(Param.INT,  "g")

