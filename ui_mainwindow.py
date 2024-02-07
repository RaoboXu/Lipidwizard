# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.6.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QButtonGroup, QCheckBox,
    QComboBox, QDoubleSpinBox, QGroupBox, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QPushButton, QRadioButton,
    QScrollArea, QSizePolicy, QSpacerItem, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_form(object):
    def setupUi(self, form):
        if not form.objectName():
            form.setObjectName(u"form")
        form.resize(865, 972)
        form.setMinimumSize(QSize(750, 0))
        self.actionLoad_File_s = QAction(form)
        self.actionLoad_File_s.setObjectName(u"actionLoad_File_s")
        self.actionLoad_Folder = QAction(form)
        self.actionLoad_Folder.setObjectName(u"actionLoad_Folder")
        self.actionDatabase = QAction(form)
        self.actionDatabase.setObjectName(u"actionDatabase")
        self.actionSplit_XCMS_Results = QAction(form)
        self.actionSplit_XCMS_Results.setObjectName(u"actionSplit_XCMS_Results")
        self.actionView_ECN = QAction(form)
        self.actionView_ECN.setObjectName(u"actionView_ECN")
        self.centralwidget = QWidget(form)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(30, -1, 30, -1)
        self.gb_databaseInfo = QWidget(self.centralwidget)
        self.gb_databaseInfo.setObjectName(u"gb_databaseInfo")
        self.horizontalLayout_3 = QHBoxLayout(self.gb_databaseInfo)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, -1, 0)
        self.label = QLabel(self.gb_databaseInfo)
        self.label.setObjectName(u"label")

        self.horizontalLayout_3.addWidget(self.label)

        self.label_databasePath = QLabel(self.gb_databaseInfo)
        self.label_databasePath.setObjectName(u"label_databasePath")

        self.horizontalLayout_3.addWidget(self.label_databasePath)

        self.label_2 = QLabel(self.gb_databaseInfo)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_3.addWidget(self.label_2)

        self.label_dbinfo = QLabel(self.gb_databaseInfo)
        self.label_dbinfo.setObjectName(u"label_dbinfo")

        self.horizontalLayout_3.addWidget(self.label_dbinfo)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_3)

        self.btnDBUpdate = QPushButton(self.gb_databaseInfo)
        self.btnDBUpdate.setObjectName(u"btnDBUpdate")

        self.horizontalLayout_3.addWidget(self.btnDBUpdate)


        self.verticalLayout_2.addWidget(self.gb_databaseInfo)

        self.gb_files = QGroupBox(self.centralwidget)
        self.gb_files.setObjectName(u"gb_files")
        self.gb_files.setMinimumSize(QSize(0, 200))
        self.horizontalLayout = QHBoxLayout(self.gb_files)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget_2 = QWidget(self.gb_files)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_4 = QVBoxLayout(self.widget_2)
        self.verticalLayout_4.setSpacing(5)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)

        self.btn_addOptionalFiles = QPushButton(self.widget_2)
        self.btn_addOptionalFiles.setObjectName(u"btn_addOptionalFiles")
        self.btn_addOptionalFiles.setMinimumSize(QSize(35, 35))
        self.btn_addOptionalFiles.setMaximumSize(QSize(35, 35))
        self.btn_addOptionalFiles.setSizeIncrement(QSize(1, 1))

        self.verticalLayout_4.addWidget(self.btn_addOptionalFiles)

        self.btn_removeOptionalFiles = QPushButton(self.widget_2)
        self.btn_removeOptionalFiles.setObjectName(u"btn_removeOptionalFiles")
        self.btn_removeOptionalFiles.setMinimumSize(QSize(35, 35))
        self.btn_removeOptionalFiles.setMaximumSize(QSize(35, 35))
        self.btn_removeOptionalFiles.setSizeIncrement(QSize(1, 1))

        self.verticalLayout_4.addWidget(self.btn_removeOptionalFiles)

        self.verticalLayout_4.setStretch(1, 1)
        self.verticalLayout_4.setStretch(2, 1)

        self.horizontalLayout.addWidget(self.widget_2)

        self.listOptionalFiles = QListWidget(self.gb_files)
        self.listOptionalFiles.setObjectName(u"listOptionalFiles")
        self.listOptionalFiles.setEditTriggers(QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed|QAbstractItemView.SelectedClicked)
        self.listOptionalFiles.setSelectionMode(QAbstractItemView.MultiSelection)

        self.horizontalLayout.addWidget(self.listOptionalFiles)

        self.widget = QWidget(self.gb_files)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(100, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.btnChoseFiles = QPushButton(self.widget)
        self.btnChoseFiles.setObjectName(u"btnChoseFiles")
        self.btnChoseFiles.setMinimumSize(QSize(0, 50))

        self.verticalLayout_3.addWidget(self.btnChoseFiles)

        self.btnDeChoseFile = QPushButton(self.widget)
        self.btnDeChoseFile.setObjectName(u"btnDeChoseFile")
        self.btnDeChoseFile.setMinimumSize(QSize(0, 50))

        self.verticalLayout_3.addWidget(self.btnDeChoseFile)


        self.horizontalLayout.addWidget(self.widget)

        self.listChosenFiles = QListWidget(self.gb_files)
        self.listChosenFiles.setObjectName(u"listChosenFiles")

        self.horizontalLayout.addWidget(self.listChosenFiles)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 10)
        self.horizontalLayout.setStretch(2, 6)
        self.horizontalLayout.setStretch(3, 10)

        self.verticalLayout_2.addWidget(self.gb_files)

        self.area_Settings = QScrollArea(self.centralwidget)
        self.area_Settings.setObjectName(u"area_Settings")
        self.area_Settings.setMinimumSize(QSize(0, 300))
        self.area_Settings.setWidgetResizable(True)
        self.scrollAreaContents = QWidget()
        self.scrollAreaContents.setObjectName(u"scrollAreaContents")
        self.scrollAreaContents.setGeometry(QRect(0, 0, 786, 1062))
        self.verticalLayout = QVBoxLayout(self.scrollAreaContents)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gb_mergeConstraints = QGroupBox(self.scrollAreaContents)
        self.gb_mergeConstraints.setObjectName(u"gb_mergeConstraints")
        self.gb_mergeConstraints.setMinimumSize(QSize(0, 80))
        self.cb_skip_merge = QCheckBox(self.gb_mergeConstraints)
        self.cb_skip_merge.setObjectName(u"cb_skip_merge")
        self.cb_skip_merge.setGeometry(QRect(20, 30, 86, 20))
        self.layoutWidget1 = QWidget(self.gb_mergeConstraints)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(20, 50, 643, 31))
        self.horizontalLayout_11 = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.label_mz_var_merg = QLabel(self.layoutWidget1)
        self.label_mz_var_merg.setObjectName(u"label_mz_var_merg")

        self.horizontalLayout_11.addWidget(self.label_mz_var_merg)

        self.spin_mz_var_merg = QDoubleSpinBox(self.layoutWidget1)
        self.spin_mz_var_merg.setObjectName(u"spin_mz_var_merg")
        self.spin_mz_var_merg.setMaximum(100000.000000000000000)
        self.spin_mz_var_merg.setSingleStep(0.010000000000000)
        self.spin_mz_var_merg.setValue(3.000000000000000)

        self.horizontalLayout_11.addWidget(self.spin_mz_var_merg)

        self.label_rt_var_merg = QLabel(self.layoutWidget1)
        self.label_rt_var_merg.setObjectName(u"label_rt_var_merg")

        self.horizontalLayout_11.addWidget(self.label_rt_var_merg)

        self.spin_rt_var_merg = QDoubleSpinBox(self.layoutWidget1)
        self.spin_rt_var_merg.setObjectName(u"spin_rt_var_merg")
        self.spin_rt_var_merg.setDecimals(4)
        self.spin_rt_var_merg.setSingleStep(0.001000000000000)
        self.spin_rt_var_merg.setValue(0.010000000000000)

        self.horizontalLayout_11.addWidget(self.spin_rt_var_merg)


        self.verticalLayout.addWidget(self.gb_mergeConstraints)

        self.gb_clustering = QGroupBox(self.scrollAreaContents)
        self.gb_clustering.setObjectName(u"gb_clustering")
        self.gb_clustering.setMinimumSize(QSize(0, 150))
        self.cb_skip_deconvolution = QCheckBox(self.gb_clustering)
        self.cb_skip_deconvolution.setObjectName(u"cb_skip_deconvolution")
        self.cb_skip_deconvolution.setGeometry(QRect(20, 30, 86, 20))
        self.layoutWidget2 = QWidget(self.gb_clustering)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(20, 60, 501, 31))
        self.horizontalLayout_5 = QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_mz_var_merg_2 = QLabel(self.layoutWidget2)
        self.label_mz_var_merg_2.setObjectName(u"label_mz_var_merg_2")

        self.horizontalLayout_5.addWidget(self.label_mz_var_merg_2)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_7)

        self.label_mz_var_merg_4 = QLabel(self.layoutWidget2)
        self.label_mz_var_merg_4.setObjectName(u"label_mz_var_merg_4")

        self.horizontalLayout_5.addWidget(self.label_mz_var_merg_4)

        self.spin_cluster_mz_var = QDoubleSpinBox(self.layoutWidget2)
        self.spin_cluster_mz_var.setObjectName(u"spin_cluster_mz_var")
        self.spin_cluster_mz_var.setDecimals(6)
        self.spin_cluster_mz_var.setMinimum(0.000000000000000)
        self.spin_cluster_mz_var.setMaximum(1.000000000000000)
        self.spin_cluster_mz_var.setSingleStep(0.000010000000000)
        self.spin_cluster_mz_var.setValue(0.000500000000000)

        self.horizontalLayout_5.addWidget(self.spin_cluster_mz_var)

        self.layoutWidget3 = QWidget(self.gb_clustering)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(20, 90, 501, 31))
        self.horizontalLayout_8 = QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.label_rt_var_merg_2 = QLabel(self.layoutWidget3)
        self.label_rt_var_merg_2.setObjectName(u"label_rt_var_merg_2")

        self.horizontalLayout_8.addWidget(self.label_rt_var_merg_2)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_8)

        self.spin_cluster_time_var = QDoubleSpinBox(self.layoutWidget3)
        self.spin_cluster_time_var.setObjectName(u"spin_cluster_time_var")
        self.spin_cluster_time_var.setDecimals(4)
        self.spin_cluster_time_var.setMaximum(1.000000000000000)
        self.spin_cluster_time_var.setSingleStep(0.010000000000000)
        self.spin_cluster_time_var.setValue(0.010000000000000)

        self.horizontalLayout_8.addWidget(self.spin_cluster_time_var)

        self.layoutWidget4 = QWidget(self.gb_clustering)
        self.layoutWidget4.setObjectName(u"layoutWidget4")
        self.layoutWidget4.setGeometry(QRect(20, 120, 721, 31))
        self.horizontalLayout_9 = QHBoxLayout(self.layoutWidget4)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.label_mr_int_2 = QLabel(self.layoutWidget4)
        self.label_mr_int_2.setObjectName(u"label_mr_int_2")

        self.horizontalLayout_9.addWidget(self.label_mr_int_2)

        self.sp_min_ri_cluster = QDoubleSpinBox(self.layoutWidget4)
        self.sp_min_ri_cluster.setObjectName(u"sp_min_ri_cluster")
        self.sp_min_ri_cluster.setDecimals(6)
        self.sp_min_ri_cluster.setMaximum(100.000000000000000)
        self.sp_min_ri_cluster.setSingleStep(1.000000000000000)

        self.horizontalLayout_9.addWidget(self.sp_min_ri_cluster)

        self.label_ma_int_2 = QLabel(self.layoutWidget4)
        self.label_ma_int_2.setObjectName(u"label_ma_int_2")

        self.horizontalLayout_9.addWidget(self.label_ma_int_2)

        self.sp_min_it_cluster = QDoubleSpinBox(self.layoutWidget4)
        self.sp_min_it_cluster.setObjectName(u"sp_min_it_cluster")
        self.sp_min_it_cluster.setDecimals(4)
        self.sp_min_it_cluster.setMaximum(100000000.000000000000000)
        self.sp_min_it_cluster.setSingleStep(1000.000000000000000)

        self.horizontalLayout_9.addWidget(self.sp_min_it_cluster)


        self.verticalLayout.addWidget(self.gb_clustering)

        self.gb_assignmentParams = QGroupBox(self.scrollAreaContents)
        self.gb_assignmentParams.setObjectName(u"gb_assignmentParams")
        self.gb_assignmentParams.setMinimumSize(QSize(0, 140))
        self.layoutWidget5 = QWidget(self.gb_assignmentParams)
        self.layoutWidget5.setObjectName(u"layoutWidget5")
        self.layoutWidget5.setGeometry(QRect(20, 40, 721, 31))
        self.horizontalLayout_10 = QHBoxLayout(self.layoutWidget5)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.label_mz_var = QLabel(self.layoutWidget5)
        self.label_mz_var.setObjectName(u"label_mz_var")

        self.horizontalLayout_10.addWidget(self.label_mz_var)

        self.spin_mz_var = QDoubleSpinBox(self.layoutWidget5)
        self.spin_mz_var.setObjectName(u"spin_mz_var")
        self.spin_mz_var.setMaximum(100000.000000000000000)
        self.spin_mz_var.setSingleStep(0.010000000000000)
        self.spin_mz_var.setValue(5.000000000000000)

        self.horizontalLayout_10.addWidget(self.spin_mz_var)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_11)

        self.layoutWidget6 = QWidget(self.gb_assignmentParams)
        self.layoutWidget6.setObjectName(u"layoutWidget6")
        self.layoutWidget6.setGeometry(QRect(20, 100, 730, 31))
        self.horizontalLayout_12 = QHBoxLayout(self.layoutWidget6)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.label_mr_int = QLabel(self.layoutWidget6)
        self.label_mr_int.setObjectName(u"label_mr_int")

        self.horizontalLayout_12.addWidget(self.label_mr_int)

        self.sp_min_ri = QDoubleSpinBox(self.layoutWidget6)
        self.sp_min_ri.setObjectName(u"sp_min_ri")
        self.sp_min_ri.setDecimals(6)
        self.sp_min_ri.setMaximum(100.000000000000000)
        self.sp_min_ri.setSingleStep(1.000000000000000)

        self.horizontalLayout_12.addWidget(self.sp_min_ri)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_10)

        self.label_ma_int = QLabel(self.layoutWidget6)
        self.label_ma_int.setObjectName(u"label_ma_int")

        self.horizontalLayout_12.addWidget(self.label_ma_int)

        self.sp_min_it = QDoubleSpinBox(self.layoutWidget6)
        self.sp_min_it.setObjectName(u"sp_min_it")
        self.sp_min_it.setDecimals(4)
        self.sp_min_it.setMaximum(100000000.000000000000000)
        self.sp_min_it.setSingleStep(1000.000000000000000)

        self.horizontalLayout_12.addWidget(self.sp_min_it)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_9)


        self.verticalLayout.addWidget(self.gb_assignmentParams)

        self.gb_ions = QGroupBox(self.scrollAreaContents)
        self.gb_ions.setObjectName(u"gb_ions")
        self.gb_ions.setMinimumSize(QSize(0, 200))

        self.verticalLayout.addWidget(self.gb_ions)

        self.gb_cats = QGroupBox(self.scrollAreaContents)
        self.gb_cats.setObjectName(u"gb_cats")
        self.gb_cats.setMinimumSize(QSize(0, 120))

        self.verticalLayout.addWidget(self.gb_cats)

        self.gb_mainclass = QGroupBox(self.scrollAreaContents)
        self.gb_mainclass.setObjectName(u"gb_mainclass")
        self.gb_mainclass.setMinimumSize(QSize(0, 300))
        self.verticalLayout_5 = QVBoxLayout(self.gb_mainclass)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.mainclassArea = QScrollArea(self.gb_mainclass)
        self.mainclassArea.setObjectName(u"mainclassArea")
        self.mainclassArea.setMaximumSize(QSize(16777215, 600))
        self.mainclassArea.setWidgetResizable(True)
        self.mainclassAreaContent = QWidget()
        self.mainclassAreaContent.setObjectName(u"mainclassAreaContent")
        self.mainclassAreaContent.setGeometry(QRect(0, 0, 734, 247))
        self.mainclassArea.setWidget(self.mainclassAreaContent)

        self.verticalLayout_5.addWidget(self.mainclassArea)


        self.verticalLayout.addWidget(self.gb_mainclass)

        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(2, 3)
        self.verticalLayout.setStretch(3, 3)
        self.verticalLayout.setStretch(4, 4)
        self.area_Settings.setWidget(self.scrollAreaContents)

        self.verticalLayout_2.addWidget(self.area_Settings)

        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout_7 = QHBoxLayout(self.groupBox)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.cb_filter_ert = QCheckBox(self.groupBox)
        self.cb_filter_ert.setObjectName(u"cb_filter_ert")

        self.horizontalLayout_7.addWidget(self.cb_filter_ert)

        self.cb_enable_ecnfilter = QCheckBox(self.groupBox)
        self.cb_enable_ecnfilter.setObjectName(u"cb_enable_ecnfilter")

        self.horizontalLayout_7.addWidget(self.cb_enable_ecnfilter)

        self.rd_conf_int = QRadioButton(self.groupBox)
        self.buttonGroup = QButtonGroup(form)
        self.buttonGroup.setObjectName(u"buttonGroup")
        self.buttonGroup.addButton(self.rd_conf_int)
        self.rd_conf_int.setObjectName(u"rd_conf_int")
        self.rd_conf_int.setChecked(True)

        self.horizontalLayout_7.addWidget(self.rd_conf_int)

        self.rd_pred_int = QRadioButton(self.groupBox)
        self.buttonGroup.addButton(self.rd_pred_int)
        self.rd_pred_int.setObjectName(u"rd_pred_int")

        self.horizontalLayout_7.addWidget(self.rd_pred_int)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_5)


        self.verticalLayout_2.addWidget(self.groupBox)

        self.widget_3 = QWidget(self.centralwidget)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout_4 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(self.widget_3)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.option_merger_level = QComboBox(self.widget_3)
        self.option_merger_level.addItem("")
        self.option_merger_level.addItem("")
        self.option_merger_level.addItem("")
        self.option_merger_level.addItem("")
        self.option_merger_level.addItem("")
        self.option_merger_level.setObjectName(u"option_merger_level")
        self.option_merger_level.setModelColumn(0)

        self.horizontalLayout_4.addWidget(self.option_merger_level)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_4)


        self.verticalLayout_2.addWidget(self.widget_3)

        self.widget_5 = QWidget(self.centralwidget)
        self.widget_5.setObjectName(u"widget_5")
        self.horizontalLayout_6 = QHBoxLayout(self.widget_5)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, -1, -1, -1)
        self.btn_alignment = QPushButton(self.widget_5)
        self.btn_alignment.setObjectName(u"btn_alignment")
        font = QFont()
        font.setUnderline(True)
        self.btn_alignment.setFont(font)
        self.btn_alignment.setStyleSheet(u"color:blue")
        self.btn_alignment.setFlat(True)

        self.horizontalLayout_6.addWidget(self.btn_alignment)

        self.label_3 = QLabel(self.widget_5)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_6.addWidget(self.label_3)

        self.spin_alignment_rt_var = QDoubleSpinBox(self.widget_5)
        self.spin_alignment_rt_var.setObjectName(u"spin_alignment_rt_var")
        self.spin_alignment_rt_var.setSingleStep(0.010000000000000)

        self.horizontalLayout_6.addWidget(self.spin_alignment_rt_var)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_6)


        self.verticalLayout_2.addWidget(self.widget_5)

        self.widget_submit = QWidget(self.centralwidget)
        self.widget_submit.setObjectName(u"widget_submit")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_submit)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.btn_submit = QPushButton(self.widget_submit)
        self.btn_submit.setObjectName(u"btn_submit")
        self.btn_submit.setMinimumSize(QSize(0, 40))

        self.horizontalLayout_2.addWidget(self.btn_submit)

        self.btn_view_results = QPushButton(self.widget_submit)
        self.btn_view_results.setObjectName(u"btn_view_results")
        self.btn_view_results.setEnabled(True)
        font1 = QFont()
        font1.setFamilies([u".AppleSystemUIFont"])
        font1.setUnderline(True)
        self.btn_view_results.setFont(font1)
        self.btn_view_results.setAutoFillBackground(False)
        self.btn_view_results.setStyleSheet(u"color:blue;")
        self.btn_view_results.setAutoDefault(False)
        self.btn_view_results.setFlat(True)

        self.horizontalLayout_2.addWidget(self.btn_view_results)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addWidget(self.widget_submit)

        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 10)
        self.verticalLayout_2.setStretch(2, 18)
        self.verticalLayout_2.setStretch(4, 1)
        self.verticalLayout_2.setStretch(5, 1)
        self.verticalLayout_2.setStretch(6, 1)
        form.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(form)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 865, 26))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName(u"menuTools")
        form.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(form)
        self.statusbar.setObjectName(u"statusbar")
        form.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menuFile.addAction(self.actionLoad_File_s)
        self.menuTools.addAction(self.actionDatabase)
        self.menuTools.addAction(self.actionView_ECN)
        self.menuTools.addAction(self.actionSplit_XCMS_Results)

        self.retranslateUi(form)

        self.option_merger_level.setCurrentIndex(0)
        self.btn_view_results.setDefault(False)


        QMetaObject.connectSlotsByName(form)
    # setupUi

    def retranslateUi(self, form):
        form.setWindowTitle(QCoreApplication.translate("form", u"MainWindow", None))
        self.actionLoad_File_s.setText(QCoreApplication.translate("form", u"Load peak list(s)", None))
        self.actionLoad_Folder.setText(QCoreApplication.translate("form", u"Load Folder", None))
        self.actionDatabase.setText(QCoreApplication.translate("form", u"View Database", None))
        self.actionSplit_XCMS_Results.setText(QCoreApplication.translate("form", u"Split Peak Lists", None))
        self.actionView_ECN.setText(QCoreApplication.translate("form", u"View ECN Profiles", None))
        self.label.setText(QCoreApplication.translate("form", u"DataBase: ", None))
        self.label_databasePath.setText(QCoreApplication.translate("form", u"database file path", None))
        self.label_2.setText(QCoreApplication.translate("form", u"Last Update: ", None))
        self.label_dbinfo.setText(QCoreApplication.translate("form", u"database Info", None))
        self.btnDBUpdate.setText(QCoreApplication.translate("form", u"Update", None))
        self.gb_files.setTitle("")
        self.btn_addOptionalFiles.setText(QCoreApplication.translate("form", u"+", None))
        self.btn_removeOptionalFiles.setText(QCoreApplication.translate("form", u"-", None))
        self.btnChoseFiles.setText(QCoreApplication.translate("form", u">>", None))
        self.btnDeChoseFile.setText(QCoreApplication.translate("form", u"<<", None))
        self.gb_mergeConstraints.setTitle(QCoreApplication.translate("form", u"Peak Merging", None))
        self.cb_skip_merge.setText(QCoreApplication.translate("form", u"Skip", None))
        self.label_mz_var_merg.setText(QCoreApplication.translate("form", u"m/z variation (ppm)", None))
        self.label_rt_var_merg.setText(QCoreApplication.translate("form", u"Retention time variation (min)", None))
        self.gb_clustering.setTitle(QCoreApplication.translate("form", u"Isotope Deconvolution", None))
        self.cb_skip_deconvolution.setText(QCoreApplication.translate("form", u"Skip", None))
        self.label_mz_var_merg_2.setText(QCoreApplication.translate("form", u"m/z variation for clustering", None))
        self.label_mz_var_merg_4.setText(QCoreApplication.translate("form", u"1.003355 +/-", None))
        self.label_rt_var_merg_2.setText(QCoreApplication.translate("form", u"Retention time variation for clustering (min)", None))
        self.label_mr_int_2.setText(QCoreApplication.translate("form", u"Min relative intensity (%)", None))
        self.label_ma_int_2.setText(QCoreApplication.translate("form", u"Min intensity (absolute)", None))
        self.gb_assignmentParams.setTitle(QCoreApplication.translate("form", u"Criteria for Assignment", None))
        self.label_mz_var.setText(QCoreApplication.translate("form", u"m/z variation (ppm)           ", None))
        self.label_mr_int.setText(QCoreApplication.translate("form", u"Min relative intensity (%)", None))
        self.label_ma_int.setText(QCoreApplication.translate("form", u"Min intensity (absolute)", None))
        self.gb_ions.setTitle(QCoreApplication.translate("form", u"Adduct Ions", None))
        self.gb_cats.setTitle(QCoreApplication.translate("form", u"Categories", None))
        self.gb_mainclass.setTitle(QCoreApplication.translate("form", u"Main Classes", None))
        self.groupBox.setTitle(QCoreApplication.translate("form", u"Retention Time Filtering", None))
        self.cb_filter_ert.setText(QCoreApplication.translate("form", u"1D RT", None))
        self.cb_enable_ecnfilter.setText(QCoreApplication.translate("form", u"2D RT", None))
        self.rd_conf_int.setText(QCoreApplication.translate("form", u"Confidence interval", None))
        self.rd_pred_int.setText(QCoreApplication.translate("form", u"Prediction interval", None))
        self.label_4.setText(QCoreApplication.translate("form", u"Result merging level", None))
        self.option_merger_level.setItemText(0, QCoreApplication.translate("form", u"Root", None))
        self.option_merger_level.setItemText(1, QCoreApplication.translate("form", u"Category", None))
        self.option_merger_level.setItemText(2, QCoreApplication.translate("form", u"Main class", None))
        self.option_merger_level.setItemText(3, QCoreApplication.translate("form", u"Subclass", None))
        self.option_merger_level.setItemText(4, QCoreApplication.translate("form", u"None", None))

        self.btn_alignment.setText(QCoreApplication.translate("form", u"Alignment", None))
        self.label_3.setText(QCoreApplication.translate("form", u"Retention time variation (min)", None))
        self.btn_submit.setText(QCoreApplication.translate("form", u"Submit", None))
        self.btn_view_results.setText(QCoreApplication.translate("form", u"View Results", None))
        self.menuFile.setTitle(QCoreApplication.translate("form", u"File", None))
        self.menuTools.setTitle(QCoreApplication.translate("form", u"Tools", None))
    # retranslateUi

