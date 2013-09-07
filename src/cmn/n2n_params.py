'''
Base container class for command line parameters
'''

from cmn.param import Param


class N2NParams(object):
    
    def __init__(self):
        self.foreground = Param(Param.BOOL, "f")
        self.verbosity  = Param(Param.BOOL, "v")
        
    def toListOfTuples(self):
        return [ val.toTuple() 
                 for val in self.__dict__.values() if val.isUsed 
               ]
        
    def toString(self):
        return " ".join([ val.toString() 
                          for val in self.__dict__.values() if val.isUsed 
                        ])