from PySide6.QtWidgets import QDialog, QLabel, QFormLayout, QHBoxLayout, QVBoxLayout, QScrollArea, QWidget, QTableWidget, QTableWidgetItem
from PySide6.QtCore import Qt, QRect
from alignment import AlignedResult
from resultnode import ResultNode
from parameter import params

class resultdetailDialog(QDialog):
    def __init__(self,parent,result:ResultNode=None, samples:list[str]=[]):
        super().__init__(parent)
        self.result:ResultNode = result
        self.samples = samples
        # enable close button
        self.setupUi()
        self.resize(900, 900)
        self.setWindowTitle("Result Detail")
        self.setWindowModality(Qt.WindowModal)

    def setupUi(self):
        self.setStyleSheet("font: 36;")
        self.horizontalLayout = QHBoxLayout(self)
        self.form_mutual_info = QFormLayout()
        self.detail_table = QTableWidget()
        header = ["lm_id","name","formula","abbreviation"]
        if params.result_merge_level < 3:
            header.append("sub class")
        if params.result_merge_level < 2:
            header.append("main class")
        if params.result_merge_level < 1:
            header.append("category")
        self.detail_table.setColumnCount(len(header))
        self.detail_table.setHorizontalHeaderLabels(header)
        self.detail_table.setRowCount(self.result.result_num())
        self.detail_table.setAlternatingRowColors(True)
        #disable edit
        self.detail_table.setEditTriggers(QTableWidget.NoEditTriggers)


        for i in range(self.result.result_num()):
            result = self.result.result_list[i]
            self.detail_table.setItem(i,0,QTableWidgetItem(str(result.lm_id)))
            self.detail_table.setItem(i,1,QTableWidgetItem(result.name))
            self.detail_table.setItem(i,2,QTableWidgetItem(result.formula))
            self.detail_table.setItem(i,3,QTableWidgetItem(result.abbreviation))
            if params.result_merge_level < 3:
                self.detail_table.setItem(i,4,QTableWidgetItem(result.sub_class))
            if params.result_merge_level < 2:
                self.detail_table.setItem(i,5,QTableWidgetItem(result.main_class))
            if params.result_merge_level < 1:
                self.detail_table.setItem(i,6,QTableWidgetItem(result.category))
        self.detail_table.resizeColumnsToContents()

        self.v_layout_detail = QVBoxLayout()
        self.v_layout_detail.addWidget(self.detail_table)


        self.form_mutual_info.addRow("m/z (theoretical): ",QLabel(str(self.result.mz_theory)))
        self.form_mutual_info.addRow("m/z (experimental): ",QLabel(str(self.result.mz_exp)))
        self.form_mutual_info.addRow("delta ppm: ",QLabel(str(self.result.del_ppm)))
        self.form_mutual_info.addRow("retention time: ",QLabel(str(self.result.retention_time)))
        self.form_mutual_info.addRow("ion: ",QLabel(self.result.ion))

        if self.result.result_num() >0:
            if params.result_merge_level > 0:
                self.form_mutual_info.addRow("category: ",QLabel(self.result.result_list[0].category))
            if params.result_merge_level > 1:
                self.form_mutual_info.addRow("main class: ",QLabel(self.result.result_list[0].main_class))
            if params.result_merge_level > 2:
                self.form_mutual_info.addRow("sub class: ",QLabel(self.result.result_list[0].sub_class))
            

        self.v_layout_mutual_info = QVBoxLayout()
        self.v_layout_mutual_info.addLayout(self.form_mutual_info)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents_3 = QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QRect(0, 0, 393, 607))
        self.verticalLayout_4 = QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.form_samples = QFormLayout()

        self.form_samples.addRow("sample name",QLabel("intensity"))

        for i in range(len(self.samples)):
            self.form_samples.addRow(self.samples[i],QLabel(str(self.result.intensity_list[i])))

        self.verticalLayout_4.addLayout(self.form_samples)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_3)

        self.v_layout_mutual_info.addWidget(self.scrollArea)

        self.horizontalLayout.addLayout(self.v_layout_mutual_info,1)

        self.horizontalLayout.addLayout(self.v_layout_detail,2)

        
