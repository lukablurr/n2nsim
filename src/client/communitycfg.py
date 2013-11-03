import cmn.config


class CommunityConfig(cmn.config.Config):
    
    SECTION = "community"
    
    def __init__(self):
        cmn.config.Config.__init__(self)
        self.max = 0
        self.max_clients = 0
        self.name_prefix = None
        self.key_prefix = None
    
    def read_vars(self, config_parser):
        self.max = self.read_int(config_parser, 'max')
        self.max_clients = self.read_int(config_parser, 'max.clients')
        self.name_prefix = self.read_string(config_parser, 'prefix.name')
        self.key_prefix = self.read_string(config_parser, 'prefix.key')

