'''
Simulated client
'''

from client.edge import Edge
from client.app import App


class ClientSim(object):
    
    def __init__(self, ip_str):
        self.ip = ip_str
        self.edge = Edge()
        self.app = App()
        
    def start(self):
        pass

