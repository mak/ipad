import idaapi,idc

from ipad.qtglue import *
from ipad.w.history import WHistory
from ipad.w.storage import WStorage
from ipad.w.tree import WTree
from ipad.w.mgmt import WMgmt

IDB_WIDGETS = [WHistory,WTree,WMgmt] 
FRESH_WIDGETS = [WStorage]

class UI(xPluginForm):

    def __init__(self,ctrl):
        super(UI,self).__init__()
        self.setupWidgets()
        self.ctrl = ctrl
        
    def OnCreate(self,form):
        self.parent = self.ConvertToQt(form,self)        
        self.PupulateForm()

        
    def Show(self,cap,opt=0):
        ## need to overwrte this so i can pass my flags,
        ## without beeing modified...
        if not opt:
            opt = idaapi.PluginForm.FORM_TAB|idaapi.PluginForm.FORM_MENU|idaapi.PluginForm.FORM_RESTORE

        idaapi.plgform_show(self.__clink__, self, cap, opt)
        
    # def OnClose(self,form):
    #     self.ctrl.ui_closed()

    def setupWidgets(self):
        if idc.GetIdbPath():
            widgs = IDB_WIDGETS
        else:
            widgs = FRESH_WIDGETS
        self._widgets = [ w(self) for w in widgs]

    def all_active(self):
        return all([w.isActiveWindow() for w in self._widgets])
        
    def _get_widget(self,n):
        for w in self._widgets:
            if w.name.lower() == n:
                return w
        return None
    
    @property
    def history(self):
        return self._get_widget('history')

    @property
    def storage(self):
        return self._get_widget('storage')


    @property
    def sessions(self):
        return self._get_widget('tree')


    def reload(self):
        self.remove_tabs()
        self.setupWidgets()
        self.add_tabs()
    
    def remove_tabs(self):
        for w in self._widgets:
            idx = self.tabs.indexOf(w)
            self.tabs.removeTab(idx)

    def add_tabs(self):
        for widget in self._widgets:
            self.tabs.addTab(widget, widget.icon, widget.name)

    def save_idb(self):
        if not idc.GetIdbPath():
            idc.Warning('There is no active idb to save')
            return
        self.ctrl.store_idb(tag)
        
            
    def setButton(self):
        if idc.GetIdbPath():
            self.save_bt = QPushButton(self.tabs)
            self.save_bt.setText('Save')
            self.save_bt.clicked.connect(self.save_idb)
        
    def PupulateForm(self):

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(False)
        self.add_tabs()
        self.setButton()
        
        layout = QVBoxLayout()
        if hasattr(self,'save_bt'):
            layout.addWidget(self.save_bt)
        layout.addWidget(self.tabs)
        self.parent.setLayout(layout)


if __name__ == '__main__':
    u = UI()
    u.Show('xxx')
