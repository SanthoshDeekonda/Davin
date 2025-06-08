from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QToolBar,
                             QAction)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal
from data_viewer import DataViewer
from Visualization import Visualization
from Report import Report
from util import load_style, resource_path
import os

class Master_Layout(QMainWindow):

    init_toolBarSignal = pyqtSignal(bool)
    
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Davin")
        self.setWindowIcon(QIcon(resource_path("assests/mainWindow/logo/Davin_Logo.png")))
        self.showMaximized()

        self.ToolBarActions = {}
        self.toolBar_initialized = False
        

        # --------- 
        self.container = QWidget() # application Elements container
        self.mainLayout = QVBoxLayout() # application main layout
        self.LayoutStack = QStackedWidget() # stack of three main widgets

        self.DataViewer = DataViewer() # Data viewer Window index (0)
        self.Visualization = Visualization(self.DataViewer.Data) # Visualization Window index (1)
        self.Report = Report() # report Window index (2)
    

        #---------- UI elements

        self.Menu_bar = self.menuBar()
        self.Tool_bar = QToolBar()



        #---------- setup functions

        self.menu_reference = self.setupMenuBar() # menu bar setup function
        self.DataViewer.dataSelected.connect(self.setupToolBar) # tool bar setup function
        



        #---------- 

        self.mainLayout.addWidget(self.LayoutStack)
        self.container.setLayout(self.mainLayout)

        self.LayoutStack.addWidget(self.DataViewer)
        self.LayoutStack.addWidget(self.Visualization)
        self.LayoutStack.addWidget(self.Report)
        
        self.LayoutStack.setCurrentIndex(0)
        self.setStyleSheet(load_style(resource_path("assests/mainWindow/themes/MainWindow.qss")))
        self.setCentralWidget(self.container)

    # implementation of setup functions

    def setupMenuBar(self) -> dict:

        menu = ["File", "Themes"]

        menu_actions_lable = {
            "File": ["CSV File", "Excel File", "Exit"],
            "Themes": ["Dark Theme", "Light Theme"]
        }

        self.menu_ref = {}
        menu_actions = {"File": [], "Themes": []}

        for menu_item in menu:
            item = self.Menu_bar.addMenu(menu_item)
            self.Menu_bar.addSeparator()
            self.menu_ref[menu_item] = item
            
        for actions in menu_actions_lable["File"]:
            action = QAction(actions, self)
            self.menu_ref["File"].addAction(action)
            menu_actions["File"].append(action)

        for actions in menu_actions_lable["Themes"]:
            action = QAction(actions, self)
            self.menu_ref["Themes"].addAction(action)
            menu_actions["Themes"].append(action)


        return menu_actions
    
    def setupToolBar(self, isSelected):
        if isSelected and not self.toolBar_initialized:
            items = ["Data", "Visualization", "Report"]
            path = resource_path("assests\mainWindow\images")
            icons = os.listdir(path)
            icons.sort()

            for i, item in enumerate(icons):
                action = QAction(QIcon(os.path.join(path,item)), items[i], self)
                self.ToolBarActions[items[i]] = action
                self.Tool_bar.addAction(action)
                self.Tool_bar.addSeparator()

            self.addToolBar(Qt.BottomToolBarArea, self.Tool_bar)
            self.toolBar_initialized = True
            self.init_toolBarSignal.emit(True)


                


