
from PySide import QtGui, QtCore
from PySide.QtGui import QIcon
import datetime,json


class WStorage(QtGui.QMainWindow):

    def __init__(self,parent):
        QtGui.QMainWindow.__init__(self)
        self.parent = parent
        self.name = 'History'
        self.icon = QIcon('')
        self.rcount = 0

        self.treeView = QtGui.QTreeView()
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.openMenu)
        
        self.model = QtGui.QStandardItemModel()
        self.addItems(self.model, data)
        self.treeView.setModel(self.model)
        
        self.model.setHorizontalHeaderLabels([self.tr("Object")])
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.treeView)
        self.setLayout(layout)
    
    def addItems(self, parent, elements):
    
        for text, children in elements:
            item = QtGui.StandardItem(text)
            parent.appendRow(item)
            if children:
                self.addItems(item, children)
    
    def openMenu(self, position):
    
        indexes = self.treeView.selectedIndexes()
        if len(indexes) > 0:
        
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1
        
        menu = QtGui.QMenu()
        if level == 0:
            menu.addAction(self.tr("Edit person"))
        elif level == 1:
            menu.addAction(self.tr("Edit object/container"))
        elif level == 2:
            menu.addAction(self.tr("Edit object"))
        
        menu.exec_(self.treeView.viewport().mapToGlobal(position))

