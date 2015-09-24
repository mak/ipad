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
        
class WMgmt(QtGui.QMainWindow):

    def __init__(self,parent):
        QtGui.QMainWindow.__init__(self)
        self.parent = parent
        self.name = 'Managment'
        self.icon = QIcon('')
        self.rcount = 0


        self.users_widg = QtGui.QWidget()
        self.users_form = QtGui.QFormLayout()
        self.users_box = QtGui.QComboBox(self.users_widg)
        self.users_box.addItems(['mak','test'])
        
        # self.refsh_bt = QtGui.QPushButton(self.treeView)
        # self.refsh_bt.setText('Refresh')
        # self.refsh_bt.clicked.connect(self.refresh)

        

        layout = QtGui.QVBoxLayout()
#        layout.addWidget(self.treeView)
        layout.addWidget(self.users_widg)

        widg=QtGui.QWidget()
        widg.setLayout(layout)
        self.setCentralWidget(widg)

    def refresh(self):
        pass
