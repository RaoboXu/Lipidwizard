# -*- coding: utf-8 -*-

################################################################################
# Form generated from reading UI file 'tableview.ui'
##
# Created by: Qt User Interface Compiler version 6.0.0
##
# WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from email import header
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import QVBoxLayout, QTableView


class Ui_DBViewWidget(object):
    def setupUi(self, DBViewWidget):
        if not DBViewWidget.objectName():
            DBViewWidget.setObjectName(u"DBViewWidget")
        DBViewWidget.resize(800, 600)
        self.verticalLayout = QVBoxLayout(DBViewWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tb_db = QTableView(DBViewWidget)
        self.tb_db.setObjectName(u"tb_db")

        self.verticalLayout.addWidget(self.tb_db)

        self.retranslateUi(DBViewWidget)

        QMetaObject.connectSlotsByName(DBViewWidget)
    # setupUi

    def retranslateUi(self, DBViewWidget):
        DBViewWidget.setWindowTitle(QCoreApplication.translate(
            "DBViewWidget", u"DBViewWidget", None))
    # retranslateUi

