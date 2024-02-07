import sys
from PySide6.QtWidgets import QHeaderView, QVBoxLayout, QWidget, QLabel, QApplication, QMessageBox
from PySide6.QtCore import Qt, QModelIndex, QRect, QAbstractItemModel
from PySide6.QtGui import QFont, QColor
from ui_treeview import Ui_form
from config import config
from molecule import Molecule
from resultnode import root


class ResultsTreeModel(QAbstractItemModel):
    def __init__(self, data:root):
        super(ResultsTreeModel,self).__init__()
        self.tree = data
        self.headers=["name","child_number"]
        pass

    def index(self,row, column, _parent:QModelIndex = None):
        if not _parent or not _parent.isValid():
            parent = self.tree
        else:
            parent = _parent.internalPointer()
        
        if not QAbstractItemModel.hasIndex(self,row,column,_parent):
            return QModelIndex()
        
        child = parent.child(row)
        if child:
            return QAbstractItemModel.createIndex(self,row,column,child)
        else:
            return QModelIndex()

    def parent(self, index:QModelIndex):
        if index.isValid():
            p = index.internalPointer().parent()
            if p:
                return QAbstractItemModel.createIndex(self,p.child_num(),0,p)
        return QModelIndex()

    def rowCount(self, index):
        if index.isValid():
            return index.internalPointer().child_num()
        else:
            return self.tree.child_num()

    def columnCount(self,index):
        if index.isValid():
            return index.internalPointer().attr_num()
        return self.tree.attr_num()

    def parent(self, index):
        if index.isValid():
            p = index.internalPointer().parent
            if p:
                return QAbstractItemModel.createIndex(self,p.child_num(),0,p)
        return QModelIndex()

    def data(self, index, role):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == Qt.DisplayRole:
            return node[index.column()]
        return None

    def headerData(self,section, orientation, role):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return self.headers[section]
        return None

    def setData(self, index, value, role):
        if not index.isValid():
            return False
        node = index.internalPointer()
        if role == Qt.EditRole:
            if value == "":
                value = None
            node[index.column()] = value
            return True
        return None

    def flags(self,index):
        flag = Qt.ItemIsEnabled
        if index.isValid() and index.column()!=1:
            flag |= Qt.ItemIsEditable | Qt.ItemIsSelectable
        return flag

class CatWideget(QWidget, Ui_form):
    def __init__(self, tree_data):
        super().__init__()
        self.setupUi(self)
        self.tree_model = ResultsTreeModel(tree_data)
        self.resultsTreeview.setModel(self.tree_model)
    def closeEvent(self,event):
        # if self.tree_model.rt_updated:
        #     msg_box = QMessageBox()
        #     msg_box.setText("Categories expected retention time range updated")
        #     msg_box.setInformativeText("Do you want to save your changes?")
        #     msg_box.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel )
        #     msg_box.setDefaultButton(QMessageBox.Save )
        #     ret = msg_box.exec()
        #     if ret == QMessageBox.Save:
        #         config.UpdateCategories()
        #     if ret == QMessageBox.Cancel:
        #         event.ignore()
        #         return
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = CatWideget(root)
    widget.showMaximized()
    sys.exit(app.exec())