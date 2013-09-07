import threading
import socket
import nfqueue
#from dpkt import ip
import debug


class Filter(threading.Thread):
    
    MAX_QUEUE_LEN = 50000
    
    def __init__(self, queue_num, simulator):
        threading.Thread.__init__(self)
        self.queueNum = queue_num
        self.simulator = simulator
        
        self.queue = nfqueue.queue()
        self.queue.set_callback(simulator.handleUdp)
        self.queue.fast_open(queue_num, socket.AF_INET)
        self.queue.set_queue_maxlen(Filter.MAX_QUEUE_LEN)
        
    def __del__(self):
        self.queue.unbind(socket.AF_INET)
        self.queue.close()
        self.queue = None
        
    def run(self):
        #debug.traceMe()
        try:
            self.queue.try_run()
        except KeyboardInterrupt as e:
            print ("interrupted")

