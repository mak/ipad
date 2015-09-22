## ida
import idc
import idaapi

import os
import hashlib
import requests
import threading
from ipad.compat import Opener,wait

class Commands(object):

    def __init__(self,plg,ch):
        self.plg = plg
        self.cfg = plg.cfg
        self.op  = Opener()
        self.ch  = ch
        
    def cmd(self,cmd,*args,**kwargs):
        if 'data' not in kwargs:
            data = {}
        else:
            data = kwargs['data']
            
        data['key']  = self.cfg.key
        data['user'] = self.cfg.user
        
        if 'uid' not in data:
            data['uid'] = self.cfg.uid
        kwargs['data'] = data

        url = 'http://localhost:8080/' + cmd
        r = requests.post(url,*args,**kwargs)
        return r

    def _relunch(self):
        ## wait 200
        wait(5)
        print '[*] please wait untill aa is finished'
        wait(15)
        self.plg._start_hooks()
        print '[+] hooks re-luched'

    def session_is_exec(self,ssid):
        return not self.cmd('get_stype',data={'ssid':ssid}).json()['r']
        
        
    def load_idb(self,uid,ssid):
        r = self.cmd('get',data={'ssid':ssid,'uid':uid})
        name = r.headers['X-IDB-Name']
        with open('/tmp/ipad/'+name,'w') as f:
            f.write(r.content)

        ## terminate ipad
        self.plg._stop_hooks()

        threading.Thread(target=self._relunch).start()
        self.op.open_file('/tmp/ipad/'+name)

    def store_idb(self):
        
        ssid = None
        try:
            ssid = self.cfg.ssid
        except AttributeError:
            ## this first store
            pass

        if not ssid:
            ssid = '0'
            p = os.path.join(os.getcwd(),idc.GetInputFile())
            
        elif self.session_is_exec(ssid):
            ssid = '0'
            p = idc.GetIdbPath()
        else:
            p = idc.GetIdbPath()
            

        with open(p) as f:
            data = f.read()
            
        h = hashlib.sha256(data).hexdigest()
        data = {'ssid':ssid,'uid':self.cfg.uid,'hash':h}
        r= self.cmd('create_idb',data=data,files={'data':open(p,'rb')}).json()
        if r['session'] != ssid:
            self.cfg.ssid = r['session']
            print self.ch
            self.ch.start()
        
