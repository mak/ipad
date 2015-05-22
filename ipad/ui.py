import idaapi
from PySide import QtGui,QtCore

from ipad.w.history import WHistory

WIDGETS = [WHistory]

class UI(idaapi.PluginForm):

    def __init__(self):
        super(UI,self).__init__()
        self.setupWidgets()
        self.QtGui = QtGui ## workaround for missing ctx in idaapi...
        
    def OnCreate(self,form):
        self.parent = self.FormToPySideWidget(form,self)
        self.PupulateForm()

        
    def OnClose(self,form):
        pass

    def setupWidgets(self):
        self._widgets = [ w(self) for w in WIDGETS]

    def _get_widget(self,n):
        for w in self._widgets:
            if w.name.lower() == n:
                return w
    @property
    def history(self):
        return self._get_widget('history')
            
    def PupulateForm(self):

        self.tabs = QtGui.QTabWidget()
        self.tabs.setTabsClosable(False)
        for widget in self._widgets:
            self.tabs.addTab(widget, widget.icon, widget.name)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.tabs)
        self.parent.setLayout(layout)


if __name__ == '__main__':
    u = UI()
    u.Show('xxx')
