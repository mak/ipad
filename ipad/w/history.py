
from PySide import QtGui, QtCore
from PySide.QtGui import QIcon
import datetime

class WHistory(QtGui.QMainWindow):

    def __init__(self,parent):
        QtGui.QMainWindow.__init__(self)
        self.parent = parent
        self.name = 'History'
        self.icon = QIcon('')
        self.rcount = 0
        
        self._prepare_list()

        # widg = QtGui.QWidget()
        # wlay = QtGui.QVBoxLayout()
        # wlay.addWidget(self.hist_list)
        # widg.setLayout(wlay)

        self.setCentralWidget(self.hist_list)
        
    def _populate(self,array):
        self.hist_list_label = ['timestamp','action']
        self.hist_list.clear()
        self.hist_list.setColumnCount(len(self.hist_list_label))
        self.hist_list.setHorizontalHeaderLabels(self.hist_list_label)
        self.hist_list.setRowCount(len(array))
            
        for row,el in enumerate(array):
            for cl,clname in enumerate(self.hist_list_label):
                if cl == 0:
                    itm = QtGui.QTableWidgetItem(str(datetime.datetime.fromtimestamp(el['timestamp'])))
                elif cl == 1:
                    itm = QtGui.QTableWidgetItem(el['action'])
                self.hist_list.setItem(row,cl,itm)
            self.hist_list.resizeRowToContents(row)
        self.hist_list.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)    
        self.hist_list.resizeColumnsToContents()


    def _append(self,el):
        nrow = self.hist_list.rowCount()
        self.hist_list.setRowCount(nrow+1)
        for cl,clname in enumerate(self.hist_list_label):
            if cl == 0:
                itm = QtGui.QTableWidgetItem(str(datetime.datetime.fromtimestamp(el['timestamp'])))
            elif cl == 1:
                itm = QtGui.QTableWidgetItem(el['action'])
            self.hist_list.setItem(nrow,cl,itm)
        self.hist_list.resizeRowToContents(nrow)
        self.hist_list.resizeColumnsToContents()
        
        
        
    def _onHistClicked(self,mi):
        print 'clicked'
            
    def _prepare_list(self):
        self.hist_list = QtGui.QTableWidget()
        self.hist_list.clicked.connect(self._onHistClicked)




