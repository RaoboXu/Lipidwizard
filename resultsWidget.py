import sys
from typing import Union
from PySide6.QtWidgets import QVBoxLayout, QWidget, QApplication, QTabWidget, QTreeView,QHeaderView,QDialog
from PySide6.QtCore import Qt, QModelIndex, QAbstractItemModel, QPersistentModelIndex
from config import config
from resultnode import ResultNode
from alignment import AlignedResult
from resultdetailWidget import resultdetailDialog
class ResultsTreeModel(QAbstractItemModel):
    def __init__(self, data:ResultNode, samples:list[str]=[], parent=None):
        super().__init__(parent)
        self.tree = data
        self.headers=config.TreeNodeTitles+samples
        self.row_count = 0

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

    def hasChildren(self, index:QModelIndex):
        if index.isValid():
            return index.internalPointer().child_num() > 0
        else:
            return self.tree.child_num() > 0

    def rowCount(self, index=QModelIndex()):
        if index.isValid():
            return index.internalPointer().child_num()
        else:
            return self.tree.child_num()

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self.headers)
    
    def parent(self, index):
        if index.isValid():
            p = index.internalPointer().parent
            if p:
                return QAbstractItemModel.createIndex(self,p.child_num(),0,p)
        return QModelIndex()

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == Qt.DisplayRole:
            return node[index.column()]

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
                value =  None
            node[index.column()] = value
            return True
        return None

    def flags(self,index):
        # allows selection and copy
        flag = Qt.ItemIsEnabled | Qt.ItemIsSelectable
        # if index.isValid() and index.column()!=1:
        #     flag |= Qt.ItemIsEditable | Qt.ItemIsSelectable
        return flag

class ResultsWidget(QWidget):
    def __init__(self, root_node:ResultNode,samples:list[str]=[]):
        super().__init__()
        self.samples=samples
        self.tabs = QTabWidget(self)
        tree_view = QTreeView(self.tabs)
        self.tree_view = tree_view
        tree_model = ResultsTreeModel(root_node,samples=samples)
        self.tree_model = tree_model
        tree_view.setModel(tree_model)
        tree_view.setAlternatingRowColors(True)
        tree_view.header().setStretchLastSection(False)
        tree_view.setUniformRowHeights(True)
        #set focused cell with solid border
        tree_view.setStyleSheet("QTreeView::item:focus{border: 1px solid green;}")
        header = tree_view.header()  # Get the header for the column
        header.setSectionResizeMode(QHeaderView.ResizeToContents)  # Resize the column to fit its content
        # set tree view header fontsize lager
        font = header.font()
        font.setPointSize(16)
        header.setFont(font)
        # set text alignment to center
        header.setDefaultAlignment(Qt.AlignCenter)
        self.tabs.addTab(tree_view,"Results Tree View")
        layout=QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)
        tree_view.doubleClicked.connect(self.tree_item_double_clicked)
        tree_view.expanded.connect(self.on_tree_collapsed_or_expanded)
        tree_view.collapsed.connect(self.on_tree_collapsed_or_expanded)

    def on_tree_collapsed_or_expanded(self,index:QModelIndex):
        max_width = 300
        header = self.tree_view.header()
        for i in range(1,self.tree_model.columnCount()):
            header.setSectionResizeMode(i,QHeaderView.ResizeToContents)
            width = self.tree_view.columnWidth(i)
            header.setSectionResizeMode(i,QHeaderView.Interactive)
            if width > max_width:
                self.tree_view.header().resizeSection(i,max_width)
        
    def closeEvent(self,event):
        super().closeEvent(event)
    
    
    def tree_item_double_clicked(self,index:QModelIndex):
        node:ResultNode = index.internalPointer()
        if node.child_num() > 0:
            return
        dialog = resultdetailDialog(self,node,self.samples)
        dialog.showMaximized()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # widget = ResultWideget(root)
    # widget.showMaximized()
    sys.exit(app.exec())