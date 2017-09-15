
import ipad.dispatch as dp 
import ipad.hooks as hooks
from ipad.db import DB


import zmq
import json
import hashlib
import datetime,threading
from copy import deepcopy

def timestamp():
    return int(datetime.datetime.now().strftime('%s'))

def get_hash(_m):
    m = deepcopy(_m)

    ## there are some fields that will change
    ## no mater what.. so remove them...
    if 'struct' in m: del m['struct']
    if 'member' in m: del m['member']
    if 'enum'   in m: del m['enum']

    d = json.dumps(m,sort_keys=True,indent=0)
    return hashlib.sha256(d).hexdigest()

class IdaAction(object):
    def __init__(self,cfg,uhist):
        self.cfg = cfg
        self.uid = cfg.uid
        self.uhist = uhist
        self._init_zmq()
        self._init_db(cfg.db)
        self._init_hooks()

        
    def _init_zmq(self):
        
        __ctx = zmq.Context()
        self.out_sock = __ctx.socket(zmq.PUB)

    def _init_db(self,db):
        self.db = DB(db)
        self.uhist.setDB(self.db)
        self.uhist.setUser(self.cfg.user)

    def _init_hooks(self):
        self.hooks = [ h(self) for h in hooks.HOOKS]
     
    def _handle_action(self,msg):

        if 'hash' not in msg:
            h = get_hash(msg)
            msg.update({'hash':h})
            
        if 'timestamp' not in msg:
            t = timestamp()
            msg.update({'timestamp':t})

        ## this is local one
        if 'user'  not in msg:
            msg.update({'user':self.cfg.user,'key':self.cfg.key,'ssid':self.cfg.ssid})
            self.out_sock.send_json(msg)
            del msg['key']; del msg['ssid']
            
        # this is remote one
        elif self.cfg.automatic:
            self.dispatch(msg)
        
        self.uhist._append(msg)
        self.db.record(msg)
        del msg

    def start(self):
        self.uhist._populate(self.db.get_all_commits())
        self.out_sock.connect(self.cfg.socket_out)
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

    def dispatch(self,data):
        self._stop_hooks()
        dp.dispatch(data)
        self._start_hooks()
