
import datetime,json
from ipad.qtglue import *

class MyItem(QTableWidgetItem):

    def __init__(self,*a,**k):
        super(MyItem,self).__init__(*a,**k)
        self.__data= None

    @property
    def xdata(self):
        return self.__data
    @xdata.setter
    def xdata(self,v):
        self.__data = v
        

class WHistory(QMainWindow):

    def __init__(self,parent):
        QMainWindow.__init__(self)
        self.parent = parent
        self.name = 'History'
        self.icon = QIcon('')
        self.rcount = 0
        
        self._prepare()

        self.hist_list.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.hist_list.customContextMenuRequested.connect(self.ctxMenu)
        self.acc_apply.triggered.connect(self.do_acc_apply)
        self.popMenu.addAction(self.acc_apply)
        self.acc_remov.triggered.connect(self.do_acc_remov)
        self.popMenu.addAction(self.acc_remov)
  
        widg = QWidget()
        wlay = QVBoxLayout()
        wlay.addWidget(self.hist_list)
        wlay.addWidget(self.hist_elem)
        widg.setLayout(wlay)

        self.setCentralWidget(widg)

    def setDB(self,db):
        self.db = db

    def setUser(self,u):
        self.user = u
        
    def _clear(self):
        self.hist_elem.clear()
        self.hist_list.clear()
        self.hist_list.setRowCount(0)
        self.hist_elem.setRowCount(0)
        self.hist_list_label = ['timestamp','action','origin']
        self.hist_list.setColumnCount(len(self.hist_list_label))
        self.hist_list.setHorizontalHeaderLabels(self.hist_list_label)

    def _populate(self,array):
        self.hist_list_label = ['timestamp','action','origin']
        self._clear()
    
        self.hist_list.setRowCount(len(array))
            
        for row,el in enumerate(array):
            for cl,clname in enumerate(self.hist_list_label):
                if cl == 0:
                    itm = MyItem(str(datetime.datetime.fromtimestamp(int(el['timestamp']))))
                elif cl == 1:
                    itm = MyItem(el['action'])
                elif cl ==2:
                    itm = MyItem('local' if el['user'] == self.user else 'remote')
                itm.xdata = el
                self.hist_list.setItem(row,cl,itm)
            self.hist_list.resizeRowToContents(row)
        self.hist_list.setSelectionMode(QAbstractItemView.SingleSelection)    
        self.hist_list.resizeColumnsToContents()


    def _append(self,el):
        nrow = self.hist_list.rowCount()
        self.hist_list.setRowCount(nrow+1)
        for cl,clname in enumerate(self.hist_list_label):
            if cl == 0:
                itm = MyItem(str(datetime.datetime.fromtimestamp(int(el['timestamp']))))
            elif cl == 1:
                itm = MyItem(el['action'])
            elif cl ==2:
                itm = MyItem('local' if el['user'] == self.user else 'remote')
            itm.xdata = el
            self.hist_list.setItem(nrow,cl,itm)
        self.hist_list.resizeRowToContents(nrow)
        self.hist_list.resizeColumnsToContents()
        
        
        
    def _onHistClicked(self,idx):

        msg = self.hist_list.itemFromIndex(idx).xdata
        # cmt =  self.db.get_commit_via_id(mi.row()+1)
        # msg = json.loads(cmt[-1])
        # msg.update({'action':cmt[1],'timestamp':cmt[0]})

        self.hist_elem_label = ['key','value']
        self.hist_elem.clear()
        self.hist_elem.setColumnCount(len(self.hist_elem_label))
        self.hist_elem.setHorizontalHeaderLabels(self.hist_elem_label)
        self.hist_elem.setRowCount(len(msg))
        for row,elm in enumerate(msg.items()):
            has_itm = False
            for cl,el in enumerate(elm):
                itm = QTableWidgetItem(str(el))
                self.hist_elem.setItem(row,cl,itm)
            self.hist_elem.resizeRowToContents(row)
        self.hist_elem.setSelectionMode(QAbstractItemView.SingleSelection)    
        self.hist_elem.resizeColumnsToContents()

            
    def _prepare(self):
        self.hist_list = QTableWidget()
        self.hist_list.clicked.connect(self._onHistClicked)
        self.hist_elem = QTableWidget()
        self.popMenu = QMenu(self)
        self.acc_apply = QAction('apply', self)
        self.acc_remov =QAction('remove', self)

        
    def ctxMenu(self,point):
        self.popMenu.exec_(self.hist_list.mapToGlobal(point))

    def do_acc_apply(self):
        indexes = self.hist_list.selectedIndexes()
        idx = indexes[0]
        data = self.hist_list.itemFromIndex(idx).xdata
        self.parent.ctrl.dispatch(data)
        
    def do_acc_remov(self):
        indexes = self.hist_list.selectedIndexes()
        idx = indexes[0]
        data = self.hist_list.itemFromIndex(idx).xdata
        print 'remove'

            
