
from hooks import HOOKS
from config import Config
from db import DB

import zmq
import datetime,threading

def timestamp():
    return int(datetime.datetime.now().strftime('%s'))

class IdaAction(object):
    def __init__(self,uid,db):
        self.uid = uid
        self._init_zmq()
        self._init_db(db)
        self._init_hooks()
        
    def _init_zmq(self):
        
        ctx = zmq.Context()
        self.out_sock = ctx.socket(zmq.PUB)

    def _init_db(self,db):
        self.db = DB(db)

    def _init_hooks(self):
        self.hooks = [ h(self) for h in HOOKS]
        
    def _handle_action(self,msg):
        t = timestamp()
        msg.update({'timestamp':t,'uid':self.uid})
        self.out_sock.send_json(msg)
        self.db.record(msg)
        del msg

    def start(self):
        self.out_sock.connect('tcp://localhost:1337')
        for h in self.hooks:
            h.hook()


        
    def end(self):
        for h in self.hooks:
            h.unhook()
            
            
        self.out_sock.close()



class changer(idaapi.plugin_t):
    flags = 0
    comment = ""
    help = ""
    wanted_name = "Changer Plugin"
    wanted_hotkey = ""

    def init(self):
        self.cfg = Config()
       # self.t = Changes(self.cfg.uid)
        self.a = IdaAction(self.cfg.uid,self.cfg.db)
        
        print '[*] start - with uid: %s and db: %s' % (self.cfg.uid,self.cfg.db)
        return idaapi.PLUGIN_OK
    
    def run(self,arg):
        #self.t.start()
        self.a.start()


    def term(self):
        self.a.end()
        #self.t.stop()
    
    

def PLUGIN_ENTRY():
  return changer()


if __name__ == '__main__':
    c = changer()
    c.init()
    c.run(0)
    
