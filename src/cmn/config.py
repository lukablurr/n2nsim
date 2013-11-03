import ConfigParser


class Config(object):
    
    SECTION = None
    
    def __init__(self):
        pass
    
    def read_from_file(self, config_file):
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        self.read_vars(config)
    
    def read_string(self, config_parser, var_name):
        return config_parser.get(self.SECTION, var_name)
    
    def read_int(self, config_parser, var_name):
        return config_parser.getint(self.SECTION, var_name)
    
    def read_float(self, config_parser, var_name):
        return config_parser.getfloat(self.SECTION, var_name)
    
    def read_bool(self, config_parser, var_name):
        return config_parser.getboolean(self.SECTION, var_name)
    
    def read_vars(self, config_parser):
        raise Exception("Abstract method")

        