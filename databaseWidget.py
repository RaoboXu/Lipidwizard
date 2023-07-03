from molecule import Molecule
from PySide6.QtWidgets import QWidget, QDialog,QVBoxLayout,QGraphicsTextItem
from PySide6.QtCore import Qt, QModelIndex, QRect, QAbstractTableModel
from PySide6.QtGui import  QColor,QPainter,QPen, QFont
# from matplotlib.lines import Line2D
from ui_tableview import Ui_form
import typing
import isotopicHelper as isohelper
from config import config
from molecule import IsotopicVariants
import numpy as np

from PySide6.QtCharts import QLineSeries, QChart, QChartView,QScatterSeries,QValueAxis

class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        self._header = data[0].args

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]
        if role == Qt.BackgroundRole and index.row() % 2 == 0:
            return QColor('darkCyan')

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

    def headerData(self, section: int, orientation: Qt.Orientation, role: int) -> typing.Any:
        r = None
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            r = self._header[section]
        else:
            r = super().headerData(section, orientation, role=role)
        return r

class IsoDistDialog(QDialog):
     def __init__(self, parent=None,iso_vars:IsotopicVariants=None, title=""):
        super().__init__(parent)
        self.setWindowTitle("Isotopic Distribution")
        self.resize(800, 600)
        self.setWindowModality(Qt.WindowModal)
        chart = QChart()
        chart.legend().setVisible(True)
        # Create a chart view and set the chart to it
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)

        peaks =[]
        for i in range(iso_vars.peakNum):
            peaks.append(iso_vars.GetPeak(i))
        peaks.sort(key=lambda peak: peak.mz)

        data_list =[]
        for peak in peaks:
            data_list.append((peak.mz,peak.rel_intensity*100))
        
        mz_grid = np.arange(peaks[0].mz-1,peaks[-1].mz+1,0.01)

        ri = np.zeros_like(mz_grid)

        sigma = 0.004

        for peak in peaks:
            ri += peak.rel_intensity * np.exp(-(mz_grid - peak.mz) ** 2 / (2 * sigma)
                                          ) / (np.sqrt(2 * np.pi) * sigma)
        
        series = QLineSeries()
        for i in range(len(ri)):
            series.append(mz_grid[i],ri[i])
        
        point_series = QScatterSeries()
        point_series.setMarkerSize(1)
        point_series.setPointLabelsVisible(True)
        point_series.setPointLabelsFormat("(@xPoint, @yPoint%)")
        font = QFont()
        font.setPointSize(15)
        point_series.setPointLabelsFont(font)
        for i_x,i_y in data_list:
            point_series.append(i_x,i_y)
            # point_series.

        chart.addSeries(series)
        chart.addSeries(point_series)
        chart.createDefaultAxes()


        x_axis = QValueAxis()

        x_axis.setTitleText("m/z")
        x_axis.setRange(int(mz_grid[0]),int(mz_grid[-1]))
        x_axis.setTickCount(int(mz_grid[0]-mz_grid[-1])+1)
        x_axis.setLabelFormat("%.0f")

        y_axis = QValueAxis()
        y_axis.setTitleText("Relative Aboundance(%)")
        y_axis.setRange(0,110)
        y_axis.setTickCount(12)
        y_axis.setLabelFormat("%.0f")

        x_axis.setLinePen(QPen(QColor("#000000"), 2, Qt.SolidLine))
        y_axis.setLinePen(QPen(QColor("#000000"), 2, Qt.SolidLine))

        chart.setAxisX(x_axis)
        chart.setAxisY(y_axis)

        # Create a chart and add the series to it
        series.attachAxis(x_axis)
        series.attachAxis(y_axis)
    
        point_series.attachAxis(x_axis)
        point_series.attachAxis(y_axis)


        chart.setTitle("Isotopic Distribution: "+title)
        # hide the legend
        chart.legend().hide()


        # Create a layout and add the chart view to it
        layout = QVBoxLayout()
        layout.addWidget(chart_view)
        self.setLayout(layout)

class DBWideget(QWidget, Ui_form):
    def __init__(self, database):
        super().__init__()
        self.setupUi(self)
        self.data: list[Molecule] = database
        self.model = TableModel(self.data)
        self.tb_db.setModel(self.model)
        self.setupSignalSlots()

    def setupSignalSlots(self):
        self.tb_db.doubleClicked.connect(self.item_doubleclicked_callback)

    def item_doubleclicked_callback(self, index: QModelIndex):
        row = index.row()
        col = index.column()
        m = self.data[row]
        ion = m.args[col]
        if ion in config.IONS:
            elements = m.getElements(withIon=True, ion=ion)
            result = isohelper.isotopic_var(elements, 5, 0)
            dg =IsoDistDialog(self,result,title=m.getValue("FORMULA")+ion)
            dg.setMinimumHeight(500)
            dg.setMinimumWidth(500)
            dg.show()
