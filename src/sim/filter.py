import threading
import socket
import nfqueue
#from dpkt import ip
import debug


class Filter(threading.Thread):
    
    MAX_PENDING = 2000
    MAX_QUEUE_LEN = 50000
    
    def __init__(self, queue_num, callback):
        threading.Thread.__init__(self)
        self.queueNum = queue_num
        
        self.queue = nfqueue.queue()
        self.queue.set_callback(callback)
        self.queue.fast_open(queue_num, socket.AF_INET)
        self.queue.set_queue_maxlen(Filter.MAX_QUEUE_LEN)
        
        self.running = False
        
    def __del__(self):
        self.queue.unbind(socket.AF_INET)
        self.queue.close()
        self.queue = None
        
    def run(self):
        debug.traceMe()
        self.running = True
        try:
            #self.queue.try_run() # blocking
            while self.running:
                self.queue.process_pending(Filter.MAX_PENDING)
        except KeyboardInterrupt as e:
            print ("interrupted")
            
    def stop(self):
        print("stopping")
        self.running = False

