import idaapi
try:
    import PySide
    PSIDES=True
except ImportError:
    PSIDES=False


if PSIDES:
    from PySide import QtGui,QtCore
    from PySide.QtCore import QProcess
    
    from PySide.QtGui import QIcon,QStandardItem,QStandardItemModel
    from PySide.QtGui import QMainWindow,QAction
    from PySide.QtGui import QTableWidgetItem
    from PySide.QtGui import QWidget,QFormLayout
    from PySide.QtGui import QComboBox,QTabWidget
    from PySide.QtGui import QVBoxLayout,QTableWidget
    from PySide.QtGui import QAbstractItemView,QMenu
    from PySide.QtGui import QPushButton,QTreeView

else:
    from PyQt5 import QtGui,QtCore
    from PyQt5.QtCore import QProcess
    
    from PyQt5.QtGui import QIcon,QStandardItem,QStandardItemModel
    from PyQt5.QtWidgets import QMainWindow,QAction
    from PyQt5.QtWidgets import QTableWidgetItem
    from PyQt5.QtWidgets import QWidget,QFormLayout
    from PyQt5.QtWidgets import QComboBox,QTabWidget
    from PyQt5.QtWidgets import QVBoxLayout,QTableWidget
    from PyQt5.QtWidgets import QAbstractItemView,QMenu
    from PyQt5.QtWidgets import QPushButton,QTreeView

# class StoreItm(object);
    
#     @property
#     def xdata(self):
#         return self.__data
#     @xdata.setter
#     def xdata(self,v):
#         self.__data = v

class xPluginForm(idaapi.PluginForm):

#    QtGui,QtCore,xPluginForm
    def ConvertToQt(self,*args,**kwargs):
        if PSIDES:
            return self.FormToPySideWidget(*args,**kwargs)
        else:
            return self.FormToPyQtWidget(*args,**kwargs)
