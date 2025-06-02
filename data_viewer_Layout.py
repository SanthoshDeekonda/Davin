from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QLabel, QPushButton, QTableWidget, 
                             QStackedLayout)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from util import load_style, DropLable, Animation_Lable

class DataViewerLayout(QWidget):
    def __init__(self):
        super().__init__()

        
        #------------- widget Elements
        self.Widget_mainLayout = QVBoxLayout()
        self.Widget_columnsInfo = QVBoxLayout()

        self.Body = QHBoxLayout()
        self.footer = QHBoxLayout()

        self.table_place_holder = DropLable()

        self.table = QTableWidget()
        self.table_stack = QStackedLayout()
        self.table_container = QWidget()

        self.data_loading_screen = Animation_Lable("assests/mainWindow/UI_GIF/Loading_Animation.gif")

        self.numeric_column_list = QListWidget()
        self.categorical_columns_list = QListWidget()

        self.table_data_info = QHBoxLayout()
        self.info = QLabel("No Data Selected")
        self.forward_btn = QPushButton("")
        self.backward_btn = QPushButton("")


        #-------------- setup functions

        self.setupBody() # body layout setup funcition
        self.setupFooter() # footer layout setup funcition



        self.setStyleSheet(load_style("assests/Data_viewer/Themes/dataViwereStyle.qss"))
        self.setLayout(self.Widget_mainLayout)

    def setupBody(self):
        self.Widget_columnsInfo.addWidget(self.numeric_column_list)
        self.Widget_columnsInfo.addWidget(self.categorical_columns_list)

        self.numeric_column_list.addItem("Numeric Data Columns: ")
        self.categorical_columns_list.addItem("Categorical Data Columns: ")

        self.Body.addLayout(self.Widget_columnsInfo, 20)
        
        place_holder = QPixmap("assests/Data_viewer/Images/No_data.png").scaled(100,100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.table_place_holder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table_place_holder.setPixmap(place_holder)

        self.table_container.setLayout(self.table_stack)
        self.table_stack.addWidget(self.table_place_holder) # index (0)
        self.table_stack.addWidget(self.table) # index (1)
        self.table_stack.addWidget(self.data_loading_screen) # index (2)


        self.Body.addWidget(self.table_container, 80)
        self.table_stack.setCurrentIndex(0)
        

        self.Widget_mainLayout.addLayout(self.Body)

    def setupFooter(self):
        self.table_data_info.addWidget(self.info, 80)

        self.backward_btn.setIcon(QIcon("assests/Data_viewer/Buttons/left-arrow.ico"))
        self.forward_btn.setIcon(QIcon("assests/Data_viewer/Buttons/right-arrow.ico"))

        self.table_data_info.addWidget(self.backward_btn, 10)
        self.table_data_info.addWidget(self.forward_btn, 10)

        self.Widget_mainLayout.addLayout(self.table_data_info)
        
