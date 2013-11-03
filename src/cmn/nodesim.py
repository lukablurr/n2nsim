'''
Simulated node
'''
from subprocess import call
from utils.net import int2ip


class NodeSim(object):
    
    CONFIG = None
    
    def __init__(self, ip, port, mport):
        self.ip = ip
        self.port = port
        self.mport = mport
        
    def localAddress(self):
        return ("%s:%d" % (int2ip(self.ip), self.port))
    
    def mgmtAddress(self):
        return ("127.0.0.1:%d" % (self.mport))
    
    def start(self):
        raise Exception("Abstract method")
    
    def stop(self):
        raise Exception("Abstract method")
        
    def addAddress(self):
        ip_args = [ "ip", "addr", "add", int2ip(self.ip), "broadcast", int2ip(self.CONFIG.ip_range.broadcast()), "dev", self.CONFIG.iface ]
        call(ip_args)

    def deleteAddress(self):#TODO remove
        ip_args = ["ip", "addr", "del", int2ip(self.ip), "dev", self.CONFIG.iface]
        call(ip_args)

