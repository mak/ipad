
import ipad.hooks as hooks
from ipad.config import Config
from ipad.db import DB
from ipad.changer import Changer
from ipad.ui import UI

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
    def __init__(self,uid,db,uhist):
        self.uid = uid
        self.uhist = uhist
        self._init_zmq()
        self._init_db(db)
        self._init_hooks()

        
    def _init_zmq(self):
        
        __ctx = zmq.Context()
        self.out_sock = __ctx.socket(zmq.PUB)

    def _init_db(self,db):
        self.db = DB(db)

    def _init_hooks(self):
        self.hooks = [ h(self) for h in hooks.HOOKS]


        
    def _handle_action(self,msg):
        t = timestamp()
        h = get_hash(msg)
        msg.update({'timestamp':t})
        self.uhist._append(msg)
        
        msg.update({'uid':self.uid,'hash':h})
        self.out_sock.send_json(msg)
        self.db.record(msg)

        del msg

    def start(self):
        self.uhist._populate(self.db.get_all_commits())
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
        self.ui = UI()
        
        self.t = Changer(self.cfg.uid) #,self.ui.parent)
#        self.t.finished.connect(self.parent)
        
        self.a = IdaAction(self.cfg.uid,self.cfg.db,self.ui.history)
        print '[*] ipad started - uid: %s | db: %s' % (self.cfg.uid,self.cfg.db)
        return idaapi.PLUGIN_OK
    
    def run(self,arg):
        self.ui.Show('ipad')
        self.t.start()
        self.a.start()

        

    def term(self):
        print '[+] going down'
        self.a.end()
        self.t.terminate()
        self.t.join()

    def __del__(self):
        super(changer,self).__del__()
        self.term()
    
        

def PLUGIN_ENTRY():
  return changer()


if __name__ == '__main__':
    c = changer()
    c.init()
    c.run(0)
    
