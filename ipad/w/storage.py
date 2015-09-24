
from PySide import QtGui, QtCore
from PySide.QtGui import QIcon
import datetime,json

class MyItem(QtGui.QStandardItem):

    def __init__(self,*a,**k):
        super(MyItem,self).__init__(*a,**k)
        self.__data= None

    @property
    def xdata(self):
        return self.__data
    @xdata.setter
    def xdata(self,v):
        self.__data = v
        
class WStorage(QtGui.QMainWindow):

    def __init__(self,parent):
        QtGui.QMainWindow.__init__(self)
        self.parent = parent
        self.name = 'Storage'
        self.icon = QIcon('')
        self.rcount = 0

        self.treeView = QtGui.QTreeView()
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.openMenu)
        self.treeView.doubleClicked.connect(self.dclick)
        self.model = QtGui.QStandardItemModel()
        self.treeView.setModel(self.model)
        
        self.model.setHorizontalHeaderLabels([self.tr("Object")])
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.treeView)
        widg=QtGui.QWidget()
        widg.setLayout(layout)
        self.setCentralWidget(widg)

        
    def _add_idb(self, n,parent, elements):
        item = QtGui.QStandardItem(n)
        parent.appendRow(item)
        for el in elements:
            tm = datetime.datetime.fromtimestamp(int(el['timestamp'])).strftime('%T %D')
            obj = MyItem('%s - %s' % (el['tag'],tm))
            obj.xdata = el
            item.appendRow(obj)
            # if children:
            #     self.addItems(item, children)

    def _populate(self,data):
        for n,v in data.iteritems():
            self._add_idb(n,self.model,v)

    def setCtrl(self,c):
        self.ctl = c

    def dclick(self,idx):
        m = idx.model()
        data = m.item(idx.column()).child(idx.row()).xdata
        self._load_idb(data)
        
    def openMenu(self, position):
    
        indexes = self.treeView.selectedIndexes()
        if len(indexes) > 0:
        
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1
                
        menu = QtGui.QMenu()
        if level == 1:
            idx = indexes[0]
            m = idx.model()
            data = m.item(idx.column()).child(idx.row()).xdata
            acc =  QtGui.QAction("Load",self)
            f_action = lambda : self._load_idb(data)
            menu.addAction(acc)
            acc.triggered.connect(f_action)
            
        menu.exec_(self.treeView.viewport().mapToGlobal(position))

    def _load_idb(self,data):
        # print data
        # print 'loaded'
        self.parent.ctrl.load_idb(data['uid'],data['ssid'])

        
