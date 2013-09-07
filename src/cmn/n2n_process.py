'''
Base class for edge and supernode wrappers
'''

import subprocess


class N2NProcess(object):
    
    PATH = None
    
    def __init__(self):
        self.params = None
        self.process = None
            
    def run(self):
        args = [ self.PATH ]
        for t in self.params.toListOfTuples():
            args.extend(t)
        self.process = subprocess.Popen(args)
        
    def stop(self):
        if not self.process:
            return
        self.process.terminate()
        self.process.wait()


