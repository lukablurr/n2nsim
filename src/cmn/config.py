import ConfigParser
from subprocess import call
from utils.iprange import IpRange
from utils.net import int2ip
from utils.tools import run_cmd


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


class NodeConfig(Config):
    
    def __init__(self):
        Config.__init__(self)
        self.path = None
        self.iface = None
        self.ip_range = None
        self.port = 0
        self.mport = 0
    
    def read_vars(self, config_parser):
        self.path = self.read_string(config_parser, 'path')
        self.iface = self.read_string(config_parser, 'iface')
        ip_range_str = self.read_string(config_parser, 'ip')
        self.ip_range = IpRange.fromString(ip_range_str)
        self.port = self.read_int(config_parser, 'port')
        self.mport = self.read_int(config_parser, 'mport')
    
    def setupIface(self, up=True):
        ''' E.g. ifconfig eth0:0 33.0.0.1 netmask 255.255.255.0 up '''
        ifconfig_args = [ "ifconfig", self.iface,
                          int2ip(self.ip_range.start),
                          "netmask", int2ip(self.ip_range.netmask()),
                          ("up" if up else "down")
                        ]
        run_cmd(ifconfig_args)
    
    def initEnvironment(self):
        self.setupIface(True)
    
    def deinitEnvironment(self):
        self.setupIface(False)

