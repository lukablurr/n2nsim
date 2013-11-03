'''
N2N Community class
'''
from client.communitycfg import CommunityConfig


class N2NCommunity(object):
    
    CONFIG = CommunityConfig()
    
    def __init__(self, name, key):
        self.name = name
        self.key = key
        self.members = []
        
    def addMember(self, clientsim):
        clientsim.edge.setCommunity(self)
        self.members.append(clientsim)
        
    def removeMember(self, clientsim):
        clientsim.edge.setCommunity(None)
        self.members.remove(clientsim)


