import zmq
import threading 

import ipad.dispatch as dp



class Changer(threading.Thread):
    def __init__(self,uid):
        super(Changer, self).__init__()
        self._stop = threading.Event()
        self.uid = uid
        
    def stop(self):
        self._stop.set()
        
    def stopped(self):
        return self._stop.isSet()

    def dispath(self,msg):
        print msg
        if not 'action' in msg:
            print '[-] wrong json...'
            return
        
        if not 'uid' in msg:
            print '[-] wrong json...'
            return
        
        if msg['uid'] == self.uid:
            ## we dont care about our msgs...
            return

        dp.dispath(msg)
        return 0
    
    def run(self):
    
        ctx = zmq.Context()
        in_sock = ctx.socket(zmq.SUB)
        in_sock.setsockopt(zmq.SUBSCRIBE,'')
        in_sock.connect('tcp://localhost:1338')

        poller = zmq.Poller()
        poller.register(in_sock,zmq.POLLIN)
        while True:
            if self.stopped(): break
            
            try:
                ev = dict(poller.poll(500))
            except zmq.ZMQError as e:
                print '0MQ exc: %s'%`e`
                break
            if in_sock in ev:
                self.dispath(in_sock.recv_json())
                
        in_sock.close()
