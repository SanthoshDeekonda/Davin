from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QStackedLayout, QLabel, QListWidget, 
                            QPushButton, QLineEdit, QSpacerItem, QSizePolicy, QListWidgetItem)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QSize
from util import DropLineEdit, load_style, DraggableListWidget, Animation_Lable


class VisualizationLayout(QWidget):

    def __init__(self):
        super().__init__()

        #--- Main Layout
        self.Visualization_MainLayout = QVBoxLayout()

        self.Visualization_ColumnsInfo = QVBoxLayout()
        self.Visualization_header = QHBoxLayout()
        self.Visualization_Body = QHBoxLayout()
        self.Visualization_footer = QHBoxLayout()

        self.Visualization_wrapper = QVBoxLayout()

        #--- UI Elements
        self.NumericList = DraggableListWidget()
        self.charList = DraggableListWidget()
        self.chartType = QListWidget()
        

        self.title_lable = QLabel("Title: ")
        self.X = QLabel("X-Lable: ")
        self.Y = QLabel("Y-Lable: ")

        self.chart_Title = QLineEdit()
        self.Xlable = DropLineEdit()
        self.Ylable = DropLineEdit()


        self.chartContainer = QWidget()
        self.chartStack = QStackedLayout()
        self.chartContainer.setLayout(self.chartStack)

        self.chart_place_holder = Animation_Lable("assests/mainWindow/UI_GIF/graph_animation.gif")
        self.Canvas = QWebEngineView()
        self.graph_loading_screen = Animation_Lable("assests/mainWindow/UI_GIF/Loading_Animation.gif")


        self.save_btn = QPushButton()
        self.download_btn = QPushButton()
        self.clear_btn = QPushButton("Clear")
        self.color_picker_btn = QPushButton()


        self.setupHeader()
        self.setupBody()
        self.setupFooter()


        self.setStyleSheet(load_style("assests/visualization/themes/visualizationLight.qss"))
        self.setLayout(self.Visualization_MainLayout)
        


    def setupHeader(self):
        self.Visualization_header.addWidget(self.title_lable)
        self.Visualization_header.addWidget(self.chart_Title)

        self.Visualization_header.addWidget(self.X)
        self.Visualization_header.addWidget(self.Xlable)

        self.Visualization_header.addWidget(self.Y)
        self.Visualization_header.addWidget(self.Ylable)

        self.Visualization_wrapper.addLayout(self.Visualization_header, 10)

    def setupBody(self):
        self.Visualization_ColumnsInfo.addWidget(self.NumericList)
        self.Visualization_ColumnsInfo.addWidget(self.charList)
        
        self.chartStack.addWidget(self.chart_place_holder) # index (0)
        self.chartStack.addWidget(self.Canvas) # index (1)
        self.chartStack.addWidget(self.graph_loading_screen) # index (2)

        self.chart_place_holder.screen.start()
        self.chartStack.setCurrentIndex(0)

        self.Visualization_wrapper.addWidget(self.chartContainer, 90)

        self.Visualization_Body.addLayout(self.Visualization_ColumnsInfo, 20)
        self.Visualization_Body.addLayout(self.Visualization_wrapper, 90)


        self.setup_chartList()
        self.Visualization_Body.addWidget(self.chartType)


        self.Visualization_MainLayout.addLayout(self.Visualization_Body)

    def setupFooter(self):

        self.Visualization_footer.addWidget(self.save_btn)
        self.Visualization_footer.addWidget(self.download_btn)
        self.Visualization_footer.addWidget(self.color_picker_btn)
        self.Visualization_footer.addWidget(self.clear_btn)

        self.save_btn.setIcon(QIcon("assests/visualization/buttons/Save.png"))
        self.color_picker_btn.setIcon(QIcon("assests/visualization/buttons/Color.png"))
        self.download_btn.setIcon(QIcon("assests/visualization/buttons/dowload.png"))


        self.Visualization_footer.addSpacerItem(QSpacerItem(40, 20,  QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        self.Visualization_MainLayout.addLayout(self.Visualization_footer)

    
    def setup_chartList(self):
        self.chartType.setIconSize(QSize(48, 48)) 
        self.chartType.setSpacing(8)               

        font = QFont("Segoe UI", 10)

        charts = [
            ("Bar Chart", "assests/visualization/images/BarChart.png"),
            ("Horizontal Bar Chart", "assests/visualization/images/HbarChart.png"),
            ("Pie Chart", "assests/visualization/images/PieChart.png"),
            ("Scatter Plot", "assests/visualization/images/ScatterPlot.png"),
            ("Line Plot", "assests/visualization/images/linePlot.png"),
            ("Histogram", "assests/visualization/images/Histogram.png"),
            ("Area Chart", "assests/visualization/images/AreaChart.png"),
            ("Box Plot", "assests/visualization/images/Box Plot.png"),
            ("Donut Chart", "assests/visualization/images/Donut_chart.png"),
            ("Waterfall", "assests/visualization/images/Waterfall_chart.png"),
            ("Treemap", "assests/visualization/images/treemap.png"),
            ("Radar Chart", "assests/visualization/images/radar_chart.png"),
            ("Bubble Chart", "assests/visualization/images/Bubble_chart.png")
        ]

        for label, path in charts:
            item = QListWidgetItem(QIcon(path), label)
            item.setFont(font)
            item.setSizeHint(QSize(160, 60))
            self.chartType.addItem(item)




