# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'treeview.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHeaderView, QSizePolicy, QTreeView,
    QVBoxLayout, QWidget)

class Ui_form(object):
    def setupUi(self, categoryTree):
        if not categoryTree.objectName():
            categoryTree.setObjectName(u"categoryTree")
        categoryTree.resize(929, 826)
        self.verticalLayout = QVBoxLayout(categoryTree)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.categoriesTreeview = QTreeView(categoryTree)
        self.categoriesTreeview.setObjectName(u"categoriesTreeview")

        self.verticalLayout.addWidget(self.categoriesTreeview)


        self.retranslateUi(categoryTree)

        QMetaObject.connectSlotsByName(categoryTree)
    # setupUi

    def retranslateUi(self, categoryTree):
        categoryTree.setWindowTitle(QCoreApplication.translate("form", u"Categories", None))
    # retranslateUi

