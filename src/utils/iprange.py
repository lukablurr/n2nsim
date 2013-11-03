from utils.net import ip2int, int2ip


class IpRange(object):
    
    def __init__(self, start, end):
        self.start = start
        self.end = end
        
    def netmask(self):
        xor = self.start ^ self.end
        bit = xor.bit_length()
        val = 0
        while bit:
            val = (val << 1) | 1
            bit -= 1
        return (val ^ 0xffffffff)
    
    def broadcast(self):
        return (self.start | self.end)
    
    def toString(self):
        return ("%s-%s" % (int2ip(self.start), int2ip(self.end)))
    
    @staticmethod
    def fromString(string):
        tokens = string.split('-')
        start = ip2int(tokens[0])
        end = ip2int(tokens[1])
        return IpRange(start, end)

