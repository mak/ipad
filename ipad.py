

import sys,os
import idc,idaapi

## my imports
from ipad.config import Config
from ipad.changer import Changer
from ipad.ui import UI
from ipad.cmd import Commands
from ipad.controler import IdaAction
## other things
import os
        
class changer(idaapi.plugin_t):
    flags = idaapi.PLUGIN_FIX | idaapi.PLUGIN_DRAW
    
    comment = "comment"
    help = "help"
    wanted_name = "Changer Plugin"
    wanted_hotkey = "alt-shift-p"

    @property
    def have_idb(self):
        return bool(idc.GetIdbPath())
    
    def init(self):
        self.ui = UI(self)
        self.load_config()
        return idaapi.PLUGIN_KEEP

    def load_config(self):

        if hasattr(self,'cfg'):
            del self.cfg
                
        self.cfg = Config()
        if not os.path.exists(self.cfg.dirname()):
            os.mkdir(self.cfg.dirname())
        self.cfg.load_cfg()
        
    def open_ui(self):
        self.ui.Show('ipad')

    def store_idb(self):
        if self.have_idb:
            idc.SaveBase(idc.GetIdbPath())
        self.cc.store_idb()
        
    def load_idb(self,*a):
        self.cc.load_idb(*a)

    def dispatch(self,d):
        self.a.dispatch(d)
        
    def run(self,arg):
        
        print '[*] ipad started - uid: %s | db: %s' % (self.cfg.uid,self.cfg.db)
                    
        if not self.have_idb:
            self.cc = Commands(self,None)#self.t)
            self.ui.storage.setCtrl(self)
            self.ui.storage._populate(self.cc.get_storage())
            self.ui.Show('ipad',UI.FORM_CENTERED|UI.FORM_MENU)
        else:            
            self.a = IdaAction(self.cfg,self.ui.history)
            self.t = Changer(self.a)
            self.cc = Commands(self.a,self.t)
            
            if not self.ui.all_active():
                self.ui.Show('ipad')
                
            if self.cc.get_changes():
                self.ui.sessions._populate(self.cc.get_sessions())
                
            self.ui.sessions.setCtrl(self.a)
            self.t.start()
            self.a.start()
            
    def term(self):
        print '[+] going down'

        if hasattr(self,'a'):
            self.a.end()
        if hasattr(self,'t'):
            self.t.quit()
        
    
def PLUGIN_ENTRY():
  return changer()


# def loadx():
#     idaapi.load_and_run_plugin(__file__,0)
    
# if __name__ == '__main__':
#     print sys.argv
#     idaapi.autoWait()


