from PySide6.QtWidgets import QVBoxLayout, QWidget, QTabWidget
from PySide6.QtCore import Qt
from PySide6.QtCharts import QLineSeries, QChart, QChartView, QScatterSeries,QValueAxis, QAreaSeries
from PySide6.QtGui import QPainter, QPen, QColor, QFont
import numpy as np
from ecn_filter import ECNProfile
class ECNWideget(QWidget):
    def __init__(self, ecn_profiles:dict[str,list[ECNProfile]]):
        super().__init__()
        # self.setupUi(self)
        self.tabs = QTabWidget(self)
        for name in ecn_profiles.keys():
            for profile in ecn_profiles[name]:
                line_series = QLineSeries()
                line_ci_l = QLineSeries()
                line_ci_l.hide()
                line_ci_u = QLineSeries()
                line_ci_u.hide()
                line_pi_l = QLineSeries()
                line_pi_l.hide()
                line_pi_u = QLineSeries()
                line_pi_u.hide()
                chart_view = QChartView(self.tabs)
                chart = QChart()
                line_series.setName("Predicted retention time")
                scatter_series = QScatterSeries()
                scatter_series.setName("Original data")
                
                # Get ECN range
                x_min, x_max = 100000.0, 0.0
                x_min = min(x_min, np.min(profile.ecn_data))
                x_max = max(x_max, np.max(profile.ecn_data))

                x_min = float(int(x_min)-2)
                x_max = float(int(x_max)+2)
                y_min, y_max = 100000.0, 0.0

                for i in np.arange(x_min,x_max,0.25):
                    y, c_i, p_i = profile.equation(i)
                    line_series.append(i,y)
                    line_ci_l.append(i,y-c_i)
                    line_ci_u.append(i,y+c_i)
                    line_pi_l.append(i,y-p_i)
                    line_pi_u.append(i,y+p_i)
                    y_min = min(y_min,y-c_i,y-p_i)
                    y_max = max(y_max,y+c_i,y+p_i)
                y_min = float(int(y_min-0.5)-0.5)
                y_max = float(int(y_max+0.5)+0.5)

                for i in range(len(profile.ecn_data)):
                    scatter_series.append(profile.ecn_data[i],profile.rt_data[i])

                area_pi = QAreaSeries(line_pi_u,line_pi_l)
                area_pi.setName("Prediction interval")
                area_pi.setColor(QColor(0,96,115,90))
                area_pi.setBorderColor(QColor(0,96,115,90))

                area_ci = QAreaSeries(line_ci_u,line_ci_l)
                area_ci.setName("Confidence interval")
                area_ci.setColor(QColor(0,96,115,90))
                area_ci.setBorderColor(QColor(0,96,115,90))

                scatter_series.setMarkerShape(QScatterSeries.MarkerShapeTriangle)
                scatter_series.setMarkerSize(14)
                scatter_series.setColor(QColor(252,149,39,255))
                scatter_series.setBorderColor(QColor(255,159,112,255))

                line_series.setColor(QColor(0,0,0,255))

                chart.addSeries(line_pi_l)
                chart.addSeries(line_pi_u)
                chart.addSeries(area_pi)

                chart.addSeries(line_ci_l)
                chart.addSeries(line_ci_u)
                chart.addSeries(area_ci)

                chart.addSeries(line_series)
                chart.addSeries(scatter_series)
                font =QFont("arial",18,QFont.Bold)   

                # Customize the chart appearance
                chart.setTitle(str(profile))
                chart.setTitleFont(font)
                chart.legend().setFont(QFont("arial",16))
                
                
                # chart.setAnimationOptions(QChart.SeriesAnimations)
                chart.createDefaultAxes()

                x_axis = chart.axes(Qt.Horizontal)[0]
                # x_axis.setRange(0, 10)
                x_axis.setTitleText("ECN")
                x_axis.setTitleFont(font)
                x_axis.setLabelsFont(font)
                x_axis.setGridLineVisible(False)

                y_axis = chart.axes(Qt.Vertical)[0]
                # y_axis.setRange(0, 10)
                y_axis.setTitleText("Retention Time (min)")
                y_axis.setTitleFont(font)
                y_axis.setLabelsFont(font)
                y_axis.setGridLineVisible(False)



                x_axis.setLinePen(QPen(QColor("#000000"), 2.5, Qt.SolidLine))
                y_axis.setLinePen(QPen(QColor("#000000"), 2.5, Qt.SolidLine))
                
                x_axis.setRange(x_min,x_max)

                tc=x_max-x_min
                while tc > 10:
                    tc/=2
                x_axis.setTickCount(2*tc+1)
                x_axis.setLabelFormat("%.1f")

                y_axis.setRange(y_min,y_max)
                tc=y_max-y_min
                while tc > 10:
                    tc/=2
                y_axis.setTickCount(2*tc+1) 
                y_axis.setLabelFormat("%.1f")

                chart_view.setChart(chart)
                chart_view.setRenderHint(QPainter.Antialiasing)
                chart_name = name
                if(chart_name != profile.name):
                    chart_name = profile.name
                self.tabs.addTab(chart_view,chart_name)

        layout=QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)
        self.windowTitle = "Expected retention time based on ECN"

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys
    from ecn_filter import ReadECNProfiles
    app = QApplication(sys.argv)
    ecn_profiles = ReadECNProfiles()

    ecn_viewer = ECNWideget(ecn_profiles)
    ecn_viewer.showMaximized()
    sys.exit(app.exec())