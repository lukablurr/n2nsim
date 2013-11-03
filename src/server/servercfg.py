from cmn.config import NodeConfig


class ServerConfig(NodeConfig):
    
    SECTION = "server"
    
    def __init__(self):
        NodeConfig.__init__(self)
        self.max = 0
    
    def read_vars(self, config_parser):
        NodeConfig.read_vars(self, config_parser)
        self.max = self.read_int(config_parser, 'max')

