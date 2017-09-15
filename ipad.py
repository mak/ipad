
## my imports
import idc
from ipad.compat import wait,test_imports
if not test_imports():
    idc.error('Failed to import needed libs')


from ipad.config import Config
from ipad.changer import Changer
from ipad.ui import UI
from ipad.cmd import Commands
from ipad.controler import IdaAction
## other things
import os


def reluch(ui):
    wait(3)
    print 'x'
    ui.Show('ipad')


class H(idaapi.UI_Hooks):

    def set_ctrl(self,ctrl):
        self.ctrl = ctrl
    
    def current_tform_changed(self,a0,a1):
        #print '--'
        t1=idaapi.get_tform_title(a0)
        t2=idaapi.get_tform_title(a1)
        if t1 == 'IDA View-A' and t2 == 'ipad':
            self.ctrl.relaunch()
        
class changer(idaapi.plugin_t):
    flags = 0
    comment = ""
    help = ""
    wanted_name = "Changer Plugin"
    wanted_hotkey = ""

    @property
    def have_idb(self):
        return bool(idc.GetIdbPath())
    
    def init(self):
        self.ui = UI(self)
        self.load_config()

        return idaapi.PLUGIN_OK

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
        self.h = H()
        self.h.set_ctrl(self)
        self.h.hook()
        self.load_data = a
        self.cc.load_idb(*a)
        
    def relaunch(self):
        self.h.unhook()
        idc.Wait()
        del self.h;
        self.ui.reload()
        self.load_config()

        self.cfg.ssid = self.load_data[1]
        self.cfg.uid = self.load_data[0]
        
        self.run(0)

    def dispatch(self,d):
        self.a.dispatch(d)
        
    def run(self,arg):
        
        print '[*] ipad started - uid: %s | db: %s' % (self.cfg.uid,self.cfg.db)
                    
        if not self.have_idb:
            self.cc = Commands(self,None)#self.t)
            self.ui.storage.setCtrl(self)
            self.ui.storage._populate(self.cc.get_storage())
            self.ui.Show('ipad',UI.FORM_CENTERED|UI.FORM_MENU|64)
        else:            
            self.a = IdaAction(self.cfg,self.ui.history)
            self.t = Changer(self.a)
            if hasattr(self,'cc'):
                self.cc.plg =self.a
                self.cc.ch = self.t
            else:
                self.cc = Commands(self.a,self.t)
            if not self.ui.all_active():
                self.ui.Show('ipad')
                
            self.cc.get_changes()
            self.ui.sessions._populate(self.cc.get_sessions())
            self.ui.sessions.setCtrl(self.a)
            self.t.start()
            self.a.start()
            
    def term(self):
        if hasattr(self,'a'):
            self.a.end()
        if hasattr(self,'t'):
            self.t.terminate()
            self.t.join()
        print '[+] going down'
        
    def __del__(self):
        self.term()
        super(changer,self).__del__()
    
        

def PLUGIN_ENTRY():
  return changer()


if __name__ == '__main__':
    c = changer()
    c.init()
    c.run(0)
    
