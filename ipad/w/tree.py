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
        
class WTree(QMainWindow):

    def __init__(self,parent):
        QMainWindow.__init__(self)
        self.parent = parent
        self.name = 'Tree'
        self.icon = QIcon('')
        self.rcount = 0

        
        self.chg_elem = QTableWidget()
                
        self.treeView = QTreeView()
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.openMenu)
        self.treeView.clicked.connect(self._onChgClicked)

        self.refsh_bt = QPushButton(self.treeView)
        self.refsh_bt.setText('Refresh')
        self.refsh_bt.clicked.connect(self.refresh)

        
        self.model = QStandardItemModel()
        self.treeView.setModel(self.model)
        
        self.model.setHorizontalHeaderLabels([self.tr("Object")])
        
        layout = QVBoxLayout()
        layout.addWidget(self.treeView)
        layout.addWidget(self.chg_elem)

        widg=QWidget()
        widg.setLayout(layout)
        self.setCentralWidget(widg)

        
    def _add_session(self, n, elements):
        item = QStandardItem(n)
        self.model.appendRow(item)
        for el in elements:
            tm = datetime.datetime.fromtimestamp(int(el['timestamp'])).strftime('%T %D')
            obj = MyItem('%s - %s - %s' % (tm,el['action'],el['user']))
            obj.xdata = el
            item.appendRow(obj)
            # if children:
            #     self.addItems(item, children)

    def _populate(self,data):
        self.model.clear()
        for ss in data:
            tm = datetime.datetime.fromtimestamp(int(ss['timestamp'])).strftime('%T %D')
            n = '%s - %s' % (ss['tag'],tm)
            self._add_session(n,ss['changes'])

    def setCtrl(self,c):
        self.ctrl = c

    def refresh(self):
        r = self.parent.ctrl.cc.get_sessions()
        self._populate(r)
        
    def openMenu(self, position):
    
        indexes = self.treeView.selectedIndexes()
        if len(indexes) > 0:
        
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1
                
        menu = QMenu()
        if level == 0:
            pass
            # acc =  QAction("",self)
            # f_action = lambda : self._load_change(data)
            # menu.addAction(acc)
            # acc.triggered.connect(f_action)
            
        elif level == 1:
            idx = indexes[0]
            m = idx.model()
            data = m.item(idx.column()).child(idx.row()).xdata
            acc =  QAction("Pick",self)
            f_action = lambda : self._load_change(data)
            menu.addAction(acc)
            acc.triggered.connect(f_action)
            
        menu.exec_(self.treeView.viewport().mapToGlobal(position))

    def _load_change(self,data):
        self.ctrl._handle_action(data)
        
    def _onChgClicked(self,idx):
        
        m = idx.model()
        msg = m.item(idx.column()).child(idx.row()).xdata
        
        # cmt =  self.db.get_commit_via_id(mi.row()+1)
        # msg = json.loads(cmt[-1])
        # msg.update({'action':cmt[1],'timestamp':cmt[0]})
        print msg
        print [ None for x in msg if x not in ['hash','timestamp','id','action'] ]
        self.chg_elem_label = ['key','value']
        self.chg_elem.clear()
        self.chg_elem.setColumnCount(len(self.chg_elem_label))
        self.chg_elem.setHorizontalHeaderLabels(self.chg_elem_label)
        self.chg_elem.setRowCount(len(msg))
        for row,elm in enumerate(msg.items()):
            for cl,el in enumerate(elm):
                itm = QTableWidgetItem(str(el))
                self.chg_elem.setItem(row,cl,itm)
            self.chg_elem.resizeRowToContents(row)
        self.chg_elem.setSelectionMode(QAbstractItemView.SingleSelection)    
        self.chg_elem.resizeColumnsToContents()
