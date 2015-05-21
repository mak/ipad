
import ipad.hooks as hooks
from ipad.config import Config
from ipad.db import DB
from ipad.changer import Changer


import zmq
import json
import hashlib
import datetime,threading

def timestamp():
    return int(datetime.datetime.now().strftime('%s'))

def get_hash(m):
    d = json.dumps(m,sort_keys=True,indent=0)
    return hashlib.sha256(d).hexdigest()

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
        self.hooks = [ h(self) for h in hooks.HOOKS]
        
    def _handle_action(self,msg):
        t = timestamp()
        h = get_hash(msg)
        msg.update({'timestamp':t,'uid':self.uid,'hash':h})
        self.out_sock.send_json(msg)
        self.db.record(msg)
        del msg

    def start(self):
        self.out_sock.connect('tcp://localhost:1337')
        self._start_hooks()
        
    def relaod_hooks(self):
        global hooks
        hooks = reload(hooks)
        self._stop_hooks()
        self._init_hooks()
        self._start_hooks()

    def _start_hooks(self):
        for h in self.hooks: h.hook()

    def _stop_hooks(self):
        for h in self.hooks: h.unhook()
                    
    def end(self):
        self._stop_hooks()
        self.out_sock.close()



class changer(idaapi.plugin_t):
    flags = 0
    comment = ""
    help = ""
    wanted_name = "Changer Plugin"
    wanted_hotkey = ""

    def init(self):
        self.cfg = Config()
        self.t = Changer(self.cfg.uid)
        self.a = IdaAction(self.cfg.uid,self.cfg.db)
        
        print '[*] start - with uid: %s and db: %s' % (self.cfg.uid,self.cfg.db)
        return idaapi.PLUGIN_OK
    
    def run(self,arg):
        self.t.start()
        self.a.start()


    def term(self):
        self.a.end()
        self.t.stop()
    
    

def PLUGIN_ENTRY():
  return changer()


if __name__ == '__main__':
    c = changer()
    c.init()
    c.run(0)
    
