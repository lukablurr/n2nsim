from cmn.config import NodeConfig


class ClientConfig(NodeConfig):
    
    SECTION = "client"
    
    def __init__(self):
        NodeConfig.__init__(self)
        self.tunIfacePrefix = None
    
    def read_vars(self, config_parser):
        NodeConfig.read_vars(self, config_parser)
        self.tunIfacePrefix = self.read_string(config_parser, 'tuniface')

