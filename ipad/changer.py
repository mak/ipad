import zmq
import json
import threading 
import ipad.dispatch as dp
from ipad.qtglue import QtCore



class Changer(QtCore.QThread):
    def __init__(self,c,p=None):
        super(Changer, self).__init__(p)
#        self._stop = threading.Event()
        self.c = c
        
    # def stop(self):
    #     self._stop.set()
        
    # def stopped(self):
    #     return self._stop.isSet()

    def dispatch(self,msg):
        print msg
        if not 'action' in msg:
            print '[-] wrong json...'
            return
        
        if not 'user' in msg:
            print '[-] wrong json...'
            return
        
        if msg['user'] == self.c.cfg.user:
            ## we dont care about our msgs...
            return

        self.c._handle_action(msg)
        return 0
    
    def run(self):

        try:
            ssid = hex(self.c.cfg.ssid).lstrip('0x')
        except AttributeError:
            print 'err'
            ## we are not attached to any session yet
            return 
        
        __ctx = zmq.Context()
        in_sock = __ctx.socket(zmq.SUB)
        in_sock.setsockopt(zmq.SUBSCRIBE,ssid)
        in_sock.connect(self.c.cfg.socket_in)

        poller = zmq.Poller()
        poller.register(in_sock,zmq.POLLIN)
        while True:
            #if self.stopped(): break
            
            try:
                ev = dict(poller.poll(500))
            except zmq.ZMQError as e:
                print '0MQ exc: %s'%`e`
                break
            if in_sock in ev:
                [_, msg] = in_sock.recv_multipart()
                print msg
                msg = json.loads(msg)
                self.dispatch(msg)
                
        in_sock.close()
