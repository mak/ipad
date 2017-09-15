## ida
import idc
import idaapi

import os
import hashlib
import requests
import threading
import tempfile
from ipad.compat import open_idb,wait

class Commands(object):

    def __init__(self,plg,ch):
        self.plg = plg
        self.cfg = plg.cfg
        self.ch  = ch
        self.server = 'http://%s:8080/' % self.cfg.server
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

        url = self.server + cmd
        r = requests.post(url,*args,**kwargs)
        return r

    def _relunch(self):
        ## wait 200
        wait(5)
        print '[*] please wait untill aa is finished'
        wait(15)
        #self.plg._start_hooks()
        print '[+] hooks re-luched'

    def session_is_exec(self,ssid):
        return not self.cmd('get_stype',data={'ssid':ssid}).json()['r']
        
        
    def load_idb(self,uid,ssid):
        r = self.cmd('get',data={'ssid':ssid,'uid':uid})
        name = r.headers['X-IDB-Name']
        if not self.session_is_exec(ssid):
            name +='.idb'

        tmpp = os.path.join(tempfile.gettempdir(),'ipad',name)
        with open(tmpp,'w') as f:
            f.write(r.content)

        ## terminate ipad
        #self.plg._stop_hooks()

        #threading.Thread(target=self._relunch).start()
        open_idb(tmpp)

    def store_idb(self):
        
        ssid = None
        try:
            ssid = self.cfg.ssid
        except AttributeError:
            ## this is first store
            pass

        if not ssid:
            ssid = '0'
            p = os.path.join(os.getcwd(),idc.GetInputFile())
            tag = 'init'
        elif self.session_is_exec(ssid):
            ssid = '0'
            p = idc.GetIdbPath()
        else:
            p = idc.GetIdbPath()
            

        if p == idc.GetIdbPath():
            tag= idc.AskStr('tag','Plase give it a name')
            if not tag:
                return
            
        with open(p) as f:
            data = f.read()
            
        h = hashlib.sha256(data).hexdigest()
        data = {'ssid':ssid,'uid':self.cfg.uid,'hash':h,'tag':tag}
        r= self.cmd('create_idb',data=data,files={'data':open(p,'rb')}).json()
        if r['session'] != ssid:
            self.cfg.ssid = r['session']
            print self.ch
            self.ch.start()
        
    def get_storage(self):
        r = self.cmd('list')
        return r.json()

    def get_changes(self):
        r = self.cmd('get_changes',data={'ssid':self.cfg.ssid})
        for msg in r.json():
            self.plg.db.record(msg)

    def get_sessions(self):
        r = self.cmd('get_idb_changes',data={'uid':self.cfg.uid})
        return r.json()
