'''
N2N Community class
'''

class N2NCommunity(object):
    
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


