from utils.net import ip2int, int2ip


class IpRange(object):
    
    def __init__(self, start, end):
        self.start = start
        self.end = end
    
    def toString(self):
        return ("%s-%s" % (int2ip(self.start), int2ip(self.end)))
    
    @staticmethod
    def fromString(string):
        tokens = string.split('-')
        start = ip2int(tokens[0])
        end = ip2int(tokens[1])
        return IpRange(start, end)

