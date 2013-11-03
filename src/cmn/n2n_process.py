'''
Base class for edge and supernode wrappers
'''

import subprocess


class N2NProcess(object):
    
    def __init__(self):
        self.params = None
        self.process = None
            
    def run(self, path):
        args = [ path ]
        for t in self.params.toListOfTuples():
            args.extend(t)
        print("Run: %s" % (" ".join(args)))
        self.process = subprocess.Popen(args)
        
    def stop(self):
        if not self.process:
            return
        self.process.terminate()
        self.process.wait()


