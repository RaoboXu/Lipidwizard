import sys
import os
import math
from parameter import params
from threading import Thread, Lock
from time import sleep
from PySide6.QtWidgets import QApplication, QMainWindow, QCheckBox, QGridLayout, QFileDialog
from PySide6.QtCore import Qt, QModelIndex, QRect
from PySide6.QtGui import QFont
from ui_mainwindow import Ui_form
from databaseWidget import DBWideget
from config import config
from typing import List, overload
import peakHelper as peakhelper
import databaseHelper as dbh
import isotopicHelper as iso
import util
from alignment import AlignedResults
from matching import SaveMatchResultCSV, matchDatabase, ReadMatchResultsCSV, SaveMatchResultCSV
from ecn_viewer import ECNWideget
from postprocessing import FilterByECN, FilterByERT, CombineSimilarResults, CombineByCategory, CombineByMainClass, CombineBySubClass, CombineBySubClassPure, CombineSimilarAlignedResults
from isotopicHelper import CalculateIsotopicProfiles, CalculateIsotopicProfilesWithCharge2
import ecn_filter
from resultsWidget import ResultsWidget
import resultnode
import csvHelper as csvh

aligned_results: AlignedResults = AlignedResults([])
aligned_results_lock = Lock()
running_proc_num: int = 0
running_proc_num_lock = Lock()

task_finished: bool = True
task_finished_lock = Lock()

need_exit: bool = False

results_tree: resultnode.ResultNode = None


class SaveAlignResultThread(Thread):
    def __init__(self, sample_num: int,  out_dir: str):
        super(SaveAlignResultThread, self).__init__()
        self.sample_num = sample_num
        self.out_dir = out_dir

    def run(self):
        global running_proc_num
        global need_exit
        global results_tree
        while running_proc_num > 0:
            if need_exit == True:
                print("exit")
                break
            sleep(2)
        results_tree = resultnode.ResultNode("root", self.sample_num)
        for r in aligned_results.rows:
            results_tree.insert_result(r)
        results_tree.save_to_csv(self.out_dir+"/aligned_result.csv",aligned_results.samples)
        header = ["name", "result number"]+aligned_results.samples
        stat_data =[]
        for i in range(1,params.result_merge_level+1):
            stat_data.extend(results_tree.stat(i)) 
        csvh.SaveDataCSV(self.out_dir+"/stat.csv",stat_data,header)
        global task_finished
        with task_finished_lock:
            task_finished = True


class MatchDatabaseThread(Thread):
    def __init__(self, peaks: List, ions: List, sample_name: str, sample_dir: str):
        super(MatchDatabaseThread, self).__init__()
        self.peaks: list = peaks
        self.ions: list[str] = ions
        self.sample_name: str = sample_name
        self.dir = sample_dir

    def run(self):
        global running_proc_num
        global aligned_results

        cluster_match_res = []
        peak_match_res = []

        peaks = peakhelper.PeakFilter(
            self.peaks, params.asmtRiMinPct/100.0, params.asmtItMin)

        if params.skipIsoDeconvolution is False:
            # clusters = peakhelper.ExtractClusters(
            #     peaks, var=params.ClusterVar, time_window=params.TimeWindowMin)
            clusters = peakhelper.ExtractClustersWithCharge2(
                peaks, var=params.ClusterVar, time_window=params.TimeWindowMin)
            peakhelper.SaveClustersCSV(
                clusters, self.dir+"/"+self.sample_name+"_Clusters.csv")
            cluster_match_res = iso.ClustersMatch(
                clusters, dbh.iso_profiles, dbh.db)
            SaveMatchResultCSV(cluster_match_res, self.dir+"/" +
                               self.sample_name+"_ClusterMatched.csv")
            # clusterRemains = [
            #     peak for peaklist in clusters for peak in peaklist if peak.intensity > 0]
            # peaks += clusterRemains
            # peaks = sorted(peaks, key=lambda peak: float(peak.mz))

        peakhelper.NormalizeIntensity(peaks)
        # peakhelper.SavePeaksCSV(peaks, self.dir+"/ToBeMatched.csv")
        peak_match_res = matchDatabase(
            dbh.db, peaks, self.ions, params.asmtMzVar)
        # SaveMatchResultCSV(resNoIso, self.dir+"/MatchedNoIso.csv")
        final_result = cluster_match_res + peak_match_res

        final_result.sort(key=lambda r: r.mz_exp)

        SaveMatchResultCSV(final_result, self.dir +
                           "/"+self.sample_name+"_GrossResult.csv")
        if params.ERTFilter:
            filteredRes = FilterByERT(final_result)
            SaveMatchResultCSV(filteredRes, self.dir+"/" +
                               self.sample_name+"_FilteredResultERT.csv")
            final_result = filteredRes

        if params.ECNFilter:
            filteredRes = FilterByECN(final_result, params.ECN_FILT_TYPE)
            SaveMatchResultCSV(filteredRes, self.dir+"/" +
                               self.sample_name+"_FilteredResultECN.csv")
            final_result = filteredRes

        SaveMatchResultCSV(final_result, self.dir +
                           "/"+self.sample_name+"_FinalResult.csv")

        for r in final_result:
            with aligned_results_lock:
                aligned_results.AddResult(r, sample_name=self.sample_name)

        peakhelper.SavePeaksCSV(peaks, self.dir+"/" +
                                self.sample_name+"_NotMatched.csv")

        print('Matching finished')
        with running_proc_num_lock:
            running_proc_num -= 1


class MainWindow(QMainWindow, Ui_form):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.optionalFiles = list()
        self.chosenFiles = list()
        self.selectedIons = list()
        self.selectedCategories = list()
        self.selectedMainClasses = list()
        self.cat_selected_num = 0
        self.dbLoaded = False
        self.setupUi(self)
        self.statusbar.showMessage('Ready')
        self.dbwidget = None
        self.ecnWidget = None
        self.resultWidget = None
        self.all_samples = []

        self.spin_mz_var_merg.setValue(params.mergMzVar)
        self.spin_rt_var_merg.setValue(params.mergRtVar)
        self.spin_mz_var.setValue(params.asmtMzVar)
        self.sp_min_ri.setValue(params.asmtRiMinPct)
        self.sp_min_it.setValue(params.asmtItMin)
        self.sp_min_it_cluster.setValue(params.stripItMin)
        self.sp_min_ri_cluster.setValue(params.stripRiMinPct)
        self.spin_cluster_mz_var.setValue(params.ClusterVar)
        self.spin_cluster_time_var.setValue(params.TimeWindowMin)
        self.spin_alignment_rt_var.setValue(params.alignmentRetentionTimeVar)
        self.cb_enable_ecnfilter.setChecked(params.ECNFilter)
        self.cb_filter_ert.setChecked(params.ERTFilter)
        self.option_merger_level.setCurrentIndex(params.result_merge_level)
        self.rd_conf_int.hide()
        self.rd_pred_int.hide()


        self.setupIonFilter()
        self.setupCategoryFilter()
        self.setupMainClassFilter()

        # self.updateScrollArea()
        self.setupSignalSlots()
        self.show()
        rec: QRect = self.listChosenFiles.geometry()
        fileWidgetWidth = rec.width()
        self.maxlen = int(fileWidgetWidth/7*0.9)

    def resizeEvent(self, event) -> None:
        rec: QRect = self.listChosenFiles.geometry()
        fileWidgetWidth = rec.width()
        self.maxlen = int(fileWidgetWidth/7*0.9)
        return super().resizeEvent(event)

    def updateDBInfo(self):
        self.databasePath = config.DatabaseCSVFile
        self.label_databasePath.setText(
            util.cutLengthOfFile(self.databasePath, 40))
        self.label_dbinfo.setText(util.getMTimeOfFile(self.databasePath))

    def setupSignalSlots(self):
        self.actionLoad_File_s.triggered.connect(self.files_add_callback)
        self.btn_addOptionalFiles.clicked.connect(self.files_add_callback)
        self.btn_removeOptionalFiles.clicked.connect(self.file_remove_callback)
        self.actionDatabase.triggered.connect(self.view_database_callback)
        self.actionView_ECN.triggered.connect(self.view_ecn)
        self.btnChoseFiles.clicked.connect(self.file_chose_callback)
        self.btnDeChoseFile.clicked.connect(self.file_dechose_callback)
        self.btnDBUpdate.clicked.connect(self.database_update_callback)
        self.actionSplit_XCMS_Results.triggered.connect(self.split_callback)
        self.btn_alignment.clicked.connect(self.alignment_callback)
        for cb in self.cbs_cate:
            cb.stateChanged.connect(self.cat_selected_change_callback)
        for cat in self.cbs_main_class:
            self.cbs_main_class[cat][0].stateChanged.connect(
                self.mainclass_all_callback)
        self.btn_submit.clicked.connect(self.submit_callback)
        self.btn_view_results.clicked.connect(self.view_results_callback)
        self.cb_enable_ecnfilter.stateChanged.connect(self.ecnfilter_callback)
        self.option_merger_level.currentIndexChanged.connect(self.merger_level_callback)
    
    def merger_level_callback(self):
        params.result_merge_level = self.option_merger_level.currentIndex()

    def ecnfilter_callback(self):
        if self.cb_enable_ecnfilter.isChecked():
            self.rd_conf_int.show()
            self.rd_pred_int.show()
        else:
            self.rd_conf_int.hide()
            self.rd_pred_int.hide()

    def loadDataBase(self):
        self.statusbar.showMessage('Loading Database...')
        dbh.database = []
        msg = dbh.readDatabaseFromCSV(config.DatabaseCSVFile, dbh.database)
        if (msg == 'SUCCESS'):
            dbh.database.sort(key=lambda molecule: float(
                molecule.getValue('EXACT_MASS')))
            self.dbLoaded = True
            self.statusbar.showMessage('database loaded')
            self.statusbar.showMessage('Ready')
            print('Load Database SUCCESS!')
        else:
            self.statusbar.showMessage(msg)
            self.statusbar.showMessage('Ready')

    def setupIonFilter(self):
        self.cb_pos_all = QCheckBox(
            text="All Positive", parent=self.gb_ions)
        self.cb_pos_all.clicked.connect(self.cb_pos_all_callback)
        self.cb_neg_all = QCheckBox(
            text="All Negative", parent=self.gb_ions)
        self.cb_neg_all.clicked.connect(self.cb_neg_all_callback)
        self.cb_neu = QCheckBox(text="Neutral", parent=self.gb_ions)
        grid_ions = QGridLayout()

        self.cbs_pos: List[QCheckBox] = []
        self.cbs_neg: List[QCheckBox] = []
        for i in range(len(config.IONS)):

            if config.ION_CHARGE[config.IONS[i]] > 0:
                cb_i = QCheckBox(config.IONS[i], parent=self.gb_ions)
                self.cbs_pos.append(cb_i)

            if config.ION_CHARGE[config.IONS[i]] < 0:
                cb_i = QCheckBox(config.IONS[i], parent=self.gb_ions)
                self.cbs_neg.append(cb_i)

        lenPos = len(self.cbs_pos)
        lenNeg = len(self.cbs_neg)
        c = 4
        row_p = math.ceil(lenPos/c)
        row_n = math.ceil(lenNeg/c)

        grid_ions.addWidget(self.cb_pos_all, 0, 0)
        grid_ions.addWidget(self.cb_neg_all, row_p, 0)
        grid_ions.addWidget(self.cb_neu, row_p+row_n, 0)
        self.cb_neu.setHidden(True)

        for row in range(row_p):
            for col in range(c):
                if row*c+col >= lenPos:
                    break
                grid_ions.addWidget(self.cbs_pos[row*c+col], row, col+1)

        for row in range(row_n):
            for col in range(c):
                if row*c+col >= lenNeg:
                    break
                grid_ions.addWidget(
                    self.cbs_neg[row*c+col], row_p+row, col+1)
        grid_ions.setVerticalSpacing(10)
        grid_ions.setHorizontalSpacing(5)
        self.gb_ions.setLayout(grid_ions)

    def setupCategoryFilter(self):
        self.cb_cate_all = QCheckBox(text="All",
                                     parent=self.gb_cats)
        grid_categories = QGridLayout()
        self.cb_cate_all.clicked.connect(self.cb_cate_all_callback)
        self.cbs_cate: List[QCheckBox] = []
        for i in range(len(config.CATEGORIES)):
            cb_i = QCheckBox(config.CATEGORIES[i],
                             parent=self.gb_cats)
            self.cbs_cate.append(cb_i)

        lenCate = len(self.cbs_cate)
        c = 3
        row = math.ceil(lenCate/c)

        grid_categories.addWidget(self.cb_cate_all, 0, 0)
        for row in range(row):
            for col in range(c):
                if row*c+col >= lenCate:
                    break
                grid_categories.addWidget(self.cbs_cate[row*c+col], row, col+1)

        self.gb_cats.setLayout(grid_categories)

    def setupMainClassFilter(self):
        if self.cat_selected_num == 0:
            self.gb_mainclass.hide()
        else:
            self.gb_mainclass.show()
        mainclass_layout = QGridLayout(self.mainclassAreaContent)
        self.mainclassAreaContent.setLayout(mainclass_layout)
        self.cbs_main_class: dict[str, List[QCheckBox]] = dict()

        for main_cls in config.MAIN_CLASSES:
            cat, cls = main_cls.split('.')
            if cat not in self.cbs_main_class.keys():
                self.cbs_main_class[cat] = []
                self.cbs_main_class[cat].append(QCheckBox(text=cat,
                                                          parent=self.mainclassAreaContent))
            self.cbs_main_class[cat].append(
                QCheckBox(text=cls, parent=self.mainclassAreaContent))

        c = 0
        for cat in self.cbs_main_class.keys():
            cbs = self.cbs_main_class[cat]
            for i in range(len(cbs)):
                if i == 0:
                    font = QFont()
                    font.setBold(True)
                    font.setPointSize((font.pointSize()+5))
                    cbs[i].setFont(font)
                self.mainclassAreaContent.layout(
                ).addWidget(self.cbs_main_class[cat][i], i, c)
            c += 1

    def updateMainClassFilter(self):
        if self.cat_selected_num == 0:
            self.gb_mainclass.hide()
        else:
            self.gb_mainclass.show()
            for cls in self.cbs_main_class.keys():
                if cls not in self.selectedCategories:
                    for i in range(len(self.cbs_main_class[cls])):
                        self.cbs_main_class[cls][i].setChecked(False)
                        self.cbs_main_class[cls][i].hide()
                else:
                    for i in range(len(self.cbs_main_class[cls])):
                        self.cbs_main_class[cls][i].setChecked(True)
                        self.cbs_main_class[cls][i].show()

    def cb_pos_all_callback(self):
        if self.cb_pos_all.checkState() == Qt.Checked:
            for i in range(len(self.cbs_pos)):
                self.cbs_pos[i].setCheckState(Qt.Checked)
        else:
            for i in range(len(self.cbs_pos)):
                self.cbs_pos[i].setCheckState(Qt.Unchecked)

    def cb_neg_all_callback(self):
        if self.cb_neg_all.checkState() == Qt.Checked:
            for i in range(len(self.cbs_neg)):
                self.cbs_neg[i].setCheckState(Qt.Checked)
        else:
            for i in range(len(self.cbs_neg)):
                self.cbs_neg[i].setCheckState(Qt.Unchecked)

    def cb_cate_all_callback(self):
        if self.cb_cate_all.checkState() == Qt.Checked:
            for i in range(len(self.cbs_cate)):
                self.cbs_cate[i].setCheckState(Qt.Checked)
        else:
            for i in range(len(self.cbs_cate)):
                self.cbs_cate[i].setCheckState(Qt.Unchecked)

    def cat_selected_change_callback(self):
        self.selectedCategories.clear()
        self.cat_selected_num = 0
        for cb in self.cbs_cate:
            if cb.isChecked():
                self.selectedCategories.append(cb.text())
                self.cat_selected_num += 1
        self.updateMainClassFilter()

    def mainclass_all_callback(self):
        for cat in config.CATEGORIES:
            if self.cbs_main_class[cat][0].isChecked():
                for i in range(len(self.cbs_main_class[cat])):
                    self.cbs_main_class[cat][i].setChecked(True)
            else:
                for i in range(len(self.cbs_main_class[cat])):
                    self.cbs_main_class[cat][i].setChecked(False)

    def files_add_callback(self):
        files = QFileDialog.getOpenFileNames(self,
                                             "Open File",
                                             "~/",
                                             "Excel Files (*.xls *.xlsx *.csv)")
        for file in files[0]:
            if file not in self.optionalFiles and file not in self.chosenFiles:
                self.optionalFiles.append(file)
        self.listOptionalFiles.clear()
        for file in self.optionalFiles:
            name = util.cutLengthOfFile(file, self.maxlen)
            self.listOptionalFiles.addItem(name)

    def file_remove_callback(self):
        selectedIndices: List[QModelIndex] = self.listOptionalFiles.selectedIndexes(
        )
        paths = []
        for i in selectedIndices:
            row = i.row()
            paths.append(self.optionalFiles[row])
        for path in paths:
            self.optionalFiles.remove(path)
        self.listOptionalFiles.clear()
        for file in self.optionalFiles:
            name = util.cutLengthOfFile(file, self.maxlen)
            self.listOptionalFiles.addItem(name)

    def file_chose_callback(self):
        selectedIndices: List[QModelIndex] = self.listOptionalFiles.selectedIndexes(
        )
        paths = []
        for i in selectedIndices:
            row = i.row()
            paths.append(self.optionalFiles[row])

        for path in paths:
            self.chosenFiles.append(path)
            self.optionalFiles.remove(path)

        self.listOptionalFiles.clear()
        for file in self.optionalFiles:
            name = util.cutLengthOfFile(file, self.maxlen)
            self.listOptionalFiles.addItem(name)

        self.listChosenFiles.clear()
        for file in self.chosenFiles:
            name = util.cutLengthOfFile(file, self.maxlen)
            self.listChosenFiles.addItem(name)

    def file_dechose_callback(self):
        selectedIndices: List[QModelIndex] = self.listChosenFiles.selectedIndexes(
        )
        paths = []
        for i in selectedIndices:
            row = i.row()
            paths.append(self.chosenFiles[row])
        for path in paths:
            self.chosenFiles.remove(path)
            self.optionalFiles.append(path)

        self.listOptionalFiles.clear()
        for file in self.optionalFiles:
            name = util.cutLengthOfFile(file, self.maxlen)
            self.listOptionalFiles.addItem(name)

        self.listChosenFiles.clear()
        for file in self.chosenFiles:
            name = util.cutLengthOfFile(file, self.maxlen)
            self.listChosenFiles.addItem(name)

    def get_parameters(self):
        params.OutputDirectory = QFileDialog.getExistingDirectory(
            self, "Where to save the aligned results", "~/", QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        params.OutputDirectory += "/MatchResults"+params.TimeStamp
        # merge peak list
        params.Catagories = self.selectedCategories
        params.MainClasses = self.selectedMainClasses
        params.Ions = self.selectedIons
        peak_list: List[List] = []
        # valid_files = list()
        params.mergMzVar = self.spin_mz_var_merg.value() * 1e-6
        params.mergRtVar = self.spin_rt_var_merg.value()
        params.ClusterVar = self.spin_cluster_mz_var.value()
        params.TimeWindowMin = self.spin_cluster_time_var.value()
        params.stripItMin = self.sp_min_it_cluster.value()
        params.stripRiMinPct = self.sp_min_ri_cluster.value()
        params.skipMerge = self.cb_skip_merge.isChecked()
        params.skipIsoDeconvolution = self.cb_skip_deconvolution.isChecked()
        params.asmtItMin = self.sp_min_it.value()
        params.asmtRiMinPct = self.sp_min_ri.value()
        params.asmtMzVar = self.spin_mz_var.value()
        params.ECNFilter = self.cb_enable_ecnfilter.isChecked()
        params.alignmentRetentionTimeVar = self.spin_alignment_rt_var.value()
        if self.rd_conf_int.isChecked():
            params.ECN_FILT_TYPE = "CONFIDENCE"
        elif self.rd_pred_int.isChecked():
            params.ECN_FILT_TYPE = "PREDICTION"
        if params.ECNFilter:
            ecn_filter.ecn_profile = ecn_filter.ReadECNProfiles()
        params.ERTFilter = self.cb_filter_ert.isChecked()
        while os.path.exists(params.OutputDirectory):
            params.OutputDirectory += "_NEW"

    def set_parameters(self):
        self.selectedCategories.clear()
        self.selectedMainClasses.clear()
        self.selectedIons.clear()
        self.spin_mz_var_merg.setValue(params.mergMzVar * 1e6)
        self.spin_rt_var_merg.setValue(params.mergRtVar)
        self.spin_cluster_mz_var.setValue(params.ClusterVar)
        self.spin_cluster_time_var.setValue(params.TimeWindowMin)
        self.sp_min_it_cluster.setValue(params.stripItMin)
        self.sp_min_ri_cluster.setValue(params.stripRiMinPct)
        self.cb_skip_merge.setChecked(params.skipMerge)
        self.cb_skip_deconvolution.setChecked(params.skipIsoDeconvolution)
        self.sp_min_it.setValue(params.asmtItMin)
        self.sp_min_ri.setValue(params.asmtRiMinPct)
        self.spin_mz_var.setValue(params.asmtMzVar)
        self.cb_enable_ecnfilter.setChecked(params.ECNFilter)
        if params.ECN_FILT_TYPE == "CONFIDENCE":
            self.rd_conf_int.setChecked(True)
        elif params.ECN_FILT_TYPE == "PREDICTION":
            self.rd_pred_int.setChecked(True)
        self.cb_filter_ert.setChecked(params.ERTFilter)

    def submit_callback(self):
        global aligned_results
        global task_finished
        with task_finished_lock:
            task_finished = False
        params.TimeStamp = util.GetTimeStamp()
        if not self.dbLoaded:
            self.statusbar.showMessage('Database is not loaded')
            return
        if len(self.chosenFiles) == 0:
            self.statusbar.showMessage('File Not Chosen', 5000)
            return
        self.statusbar.showMessage('Matching...')
        self.selectedMainClasses.clear()
        for cat in self.cbs_main_class:
            for cb in self.cbs_main_class[cat]:
                if cb.isChecked() and self.cbs_main_class[cat].index(cb) != 0:
                    self.selectedMainClasses.append(cb.text())
        self.selectedIons.clear()
        for cb_ion in self.cbs_pos:
            if cb_ion.isChecked():
                self.selectedIons.append(cb_ion.text())
        for cb_ion in self.cbs_neg:
            if cb_ion.isChecked():
                self.selectedIons.append(cb_ion.text())
        if self.cb_neu.isChecked():
            self.selectedIons.append("Neutral")
        self.get_parameters()
        os.makedirs(params.OutputDirectory)
        self.all_samples: list[str] = []
        all_dir = []
        peak_list: List[List] = []
        for source in self.chosenFiles:
            sample_name = util.GetNameOfFile(source)
            self.all_samples.append(sample_name)
            data = peakhelper.ReadPeaksCSV(source)
            peaks = list()
            if params.skipMerge is not True and (params.mergMzVar > 0 or params.mergRtVar > 0):
                print("Start merging peaks")
                peaks = peakhelper.MergePeaks(data)
                print("\nMerging peaks done!\n")
            else:
                peaks = data
            peak_list.append(peaks)
            sample_dir, sample_name = os.path.split(source)
            dotP = sample_name.rfind('.')
            sample_name = sample_name[0:dotP]
            dir_path = os.path.join(params.OutputDirectory, sample_name)
            os.makedirs(dir_path)
            all_dir.append(dir_path)
            data.sort(key=lambda peak: peak.mz)
            peakhelper.SavePeaksCSV(
                peaks, '{}/{}_merged.csv'.format(dir_path, sample_name))
            params.Save(dir_path, sample_name)

        # filter database
        aligned_results = AlignedResults(self.all_samples)
        dbh.db = dbh.FilterByClass(
            dbh.database, self.selectedCategories, self.selectedMainClasses)
        if params.skipIsoDeconvolution is False:
            dbh.iso_profiles = CalculateIsotopicProfilesWithCharge2(dbh.db, params.Ions)
            dbh.iso_profiles.sort(key=lambda iso: float(iso.M0))
        # filter peaks
        print('Rows of database need to be matched: ' + str(len(dbh.db)))
        match_thread: list[MatchDatabaseThread] = []
        global running_proc_num
        running_proc_num = len(peak_list)

        for i in range(len(peak_list)):
            match_thread.append(MatchDatabaseThread(
                peak_list[i], self.selectedIons, self.all_samples[i], all_dir[i]))

        for t in match_thread:
            t.start()

        align_thread = SaveAlignResultThread(len(
            self.all_samples), params.OutputDirectory)
        align_thread.start()
        self.statusbar.showMessage('Ready')

    def database_update_callback(self):
        self.statusbar.showMessage("Updating database")
        t = LoadDatabaseThread(self, True)
        t.start()

    def view_ecn(self):
        print("View ECN profiles")
        ecn_filter.ecn_profile = ecn_filter.ReadECNProfiles()
        self.ecnWidget = ECNWideget(ecn_profiles=ecn_filter.ecn_profile)
        self.ecnWidget.showMaximized()

    def split_callback(self):
        filename = QFileDialog.getOpenFileName(self,
                                               "Open File",
                                               "~/",
                                               "Excel Files (*.xls *.xlsx)")
        folder = os.path.dirname(filename[0])
        peakhelper.SplitTable(filename[0], folder)

    def alignment_callback(self):
        global aligned_results
        global results_tree
        params.TimeStamp = util.GetTimeStamp()
        params.alignmentRetentionTimeVar = self.spin_alignment_rt_var.value()
        self.statusBar().showMessage("alignment", 5)
        params.OutputDirectory = QFileDialog.getExistingDirectory(
            self, "Where to save the aligned results", "~/", QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if params.OutputDirectory == "":
            print("Target saving directory is not chosen")
            return
        self.all_samples: list[str] = []
        for source in self.chosenFiles:
            sample_name = util.GetNameOfFile(source)
            while sample_name in self.all_samples:
                sample_name += "_DUP"
            self.all_samples.append(sample_name)
        aligned_results = AlignedResults(self.all_samples)

        for i in range(len(self.chosenFiles)):
            data = ReadMatchResultsCSV(self.chosenFiles[i])
            for row in data:
                aligned_results.AddResult(
                    row, sample_name=self.all_samples[i])
            print("{}/{} files have been processed".format(i+1,
                  len(self.all_samples)))


        results_tree = resultnode.ResultNode("root", len(self.all_samples))
        for r in aligned_results.rows:
            results_tree.insert_result(r)
            
        results_tree.save_to_csv("{}/{}_aligned_result.csv".format(params.OutputDirectory, params.TimeStamp),aligned_results.samples)
        header = ["name", "result number"]+aligned_results.samples
        stat_data =[]
        for i in range(1,params.result_merge_level+1):
            stat_data.extend(results_tree.stat(i)) 
        csvh.SaveDataCSV("{}/{}_stat.csv".format(params.OutputDirectory, params.TimeStamp),stat_data,header)


    def view_database_callback(self):
        print('View Database')
        if self.dbLoaded:
            if self.dbwidget is None:
                self.dbwidget = DBWideget(dbh.database)
            self.dbwidget.showMaximized()
        else:
            self.statusbar.showMessage('database not loaded', 3000)

    def view_results_callback(self):
        print("View matching results")
        global results_tree
        global task_finished
        if task_finished and results_tree is not None:
            self.resultWidget = ResultsWidget(results_tree, self.all_samples)
            self.resultWidget.showMaximized()
        else:
            self.statusbar.showMessage("Results not ready", 3000)


class LoadDatabaseThread(Thread):
    def __init__(self, window: MainWindow, update=False):
        super(LoadDatabaseThread, self).__init__()
        self.w = window
        self.update = update

    def run(self):
        if self.update:
            dbh.UpdateDatabase()
        self.w.loadDataBase()
        self.w.updateDBInfo()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    thread = LoadDatabaseThread(w)
    thread.start()
    sys.exit(app.exec())
