# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tableview.ui'
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QSizePolicy, QTableView,
    QVBoxLayout, QWidget)

class Ui_form(object):
    def setupUi(self, databaseTable):
        if not databaseTable.objectName():
            databaseTable.setObjectName(u"databaseTable")
        databaseTable.resize(800, 600)
        self.verticalLayout = QVBoxLayout(databaseTable)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tb_db = QTableView(databaseTable)
        self.tb_db.setObjectName(u"tb_db")

        self.verticalLayout.addWidget(self.tb_db)


        self.retranslateUi(databaseTable)

        QMetaObject.connectSlotsByName(databaseTable)
    # setupUi

    def retranslateUi(self, databaseTable):
        databaseTable.setWindowTitle(QCoreApplication.translate("form", u"DatabaseTable", None))
    # retranslateUi

