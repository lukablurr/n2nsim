'''
Base class for command line parameters
'''


class Param(object):
    
    NONE = 0
    INT  = 1
    STR  = 2
    BOOL = 3
    
    def __init__(self, par_type, name, value = None, used = False):
        self.type = par_type
        self.name = name
        self.value = ( value if value else self.defaultValue() )
        self.isUsed = used
        
    def enable(self):
        self.isUsed = True
        
    def disable(self):
        self.isUsed = False
        
    def defaultValue(self):
        if self.type == Param.INT:
            return 0
        elif self.type == Param.STR:
            return ""
        elif self.type == Param.BOOL:
            return False
        return None
        
    def setValue(self, value):
        if (self.type == Param.INT and type(value) is not int) or \
           (self.type == Param.STR and type(value) is not str) or \
           (self.type == Param.BOOL and type(value) is not bool):
            raise Exception("Invalid value")
        
        self.value = ( value if value else self.defaultValue() )
        self.isUsed = True
    
    def getStringValue(self):
        if self.type in [Param.INT, Param.STR]:
            return str(self.value)
        return ""
    
    def option(self):
        return ("-" + self.name)
    
    def toTuple(self):
        if self.type == Param.BOOL:
            return (self.option(), )
        return (self.option(), self.getStringValue())
    
    def toString(self):
        return " ".join([self.option(), self.getStringValue()])

