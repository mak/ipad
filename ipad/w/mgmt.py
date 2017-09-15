
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
        
class WMgmt(QMainWindow):

    def __init__(self,parent):
        QMainWindow.__init__(self)
        self.parent = parent
        self.name = 'Managment'
        self.icon = QIcon('')
        self.rcount = 0


        self.users_widg = QWidget()
        self.users_form = QFormLayout()
        self.users_box = QComboBox(self.users_widg)
        self.users_box.addItems(['mak','test'])
        
        # self.refsh_bt = QtGui.QPushButton(self.treeView)
        # self.refsh_bt.setText('Refresh')
        # self.refsh_bt.clicked.connect(self.refresh)

        

        layout = QVBoxLayout()
#        layout.addWidget(self.treeView)
        layout.addWidget(self.users_widg)

        widg=QWidget()
        widg.setLayout(layout)
        self.setCentralWidget(widg)

    def refresh(self):
        pass
