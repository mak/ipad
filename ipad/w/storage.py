import datetime,json
from ipad.qtglue import *

class MyItem(QStandardItem):

    def __init__(self,*a,**k):
        super(MyItem,self).__init__(*a,**k)
        self.__data= None

    @property
    def xdata(self):
        return self.__data
    @xdata.setter
    def xdata(self,v):
        self.__data = v
        
class WStorage(QMainWindow):

    def __init__(self,parent):
        QMainWindow.__init__(self)
        self.parent = parent
        self.name = 'Storage'
        self.icon = QIcon('')
        self.rcount = 0

        self.treeView = QTreeView()
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.openMenu)
        self.treeView.doubleClicked.connect(self.dclick)
        self.model = QStandardItemModel()
        self.treeView.setModel(self.model)
        
        self.model.setHorizontalHeaderLabels([self.tr("Object")])
        
        layout = QVBoxLayout()
        layout.addWidget(self.treeView)
        widg=QWidget()
        widg.setLayout(layout)
        self.setCentralWidget(widg)

        
    def _add_idb(self, n,parent, elements):
        item = QStandardItem(n)
        parent.appendRow(item)
        for el in elements:
            tm = datetime.datetime.fromtimestamp(int(el['timestamp'])).strftime('%H:%M:%S %m/%d/%Y')
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
                
        menu = QMenu()
        if level == 1:
            idx = indexes[0]
            m = idx.model()
            data = m.item(idx.column()).child(idx.row()).xdata
            acc =  QAction("Load",self)
            f_action = lambda : self._load_idb(data)
            menu.addAction(acc)
            acc.triggered.connect(f_action)
            
        menu.exec_(self.treeView.viewport().mapToGlobal(position))

    def _load_idb(self,data):
        # print data
        # print 'loaded'
        self.parent.ctrl.load_idb(data['uid'],data['ssid'])

        
