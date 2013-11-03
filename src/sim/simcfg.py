import cmn.config


class SimulatorConfig(cmn.config.Config):
    
    SECTION = "simulator"
    
    def __init__(self):
        cmn.config.Config.__init__(self)
        self.queue = None
    
    def read_vars(self, config_parser):
        self.queue = self.read_int(config_parser, 'queue')

