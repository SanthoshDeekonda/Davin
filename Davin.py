from master_layout import Master_Layout
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from util import show_message, load_style
from splashscreen import SplashScreen
import os
import shutil
import sys


class init_davin(QThread):

    current_state = pyqtSignal(str)
    finished_setup = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.x = [str(x) for x in range(101)]
        self.y = [y for y in range(101)]
        self.path = "__demo__.png"


    def run(self):
        self.current_state.emit("Gathering resources....")
        import plotly.graph_objects as go

        self.current_state.emit("Preparing workspace....")
        fig = go.Figure(data=[go.Bar(x=self.x, y=self.y, marker_color="#03A9F4")])

        self.current_state.emit("Optimizing modules....")
        fig.write_image(self.path, format="png")

        if os.path.exists(self.path):
            os.remove(self.path)
        
        self.current_state.emit("Initialization complete....")
        self.finished_setup.emit()
        


class Davin_Core(Master_Layout):

    setup_status = pyqtSignal(str)
    setup_complete = pyqtSignal()

    def __init__(self):
        super().__init__()
        
        self.init_menuBar()
        self.init_toolBarSignal.connect(self.init_toolBar)
        self.setTempDir()

        # --------- passing data with signals
        self.DataViewer.passData.connect(self.Visualization.getData)
        self.DataViewer.passColumns.connect(self.Visualization.getColumnItems)
        self.Visualization.saved_visualization.connect(self.Report.getSavedChart)


    def init_menuBar(self):
        for actions in self.menu_reference:
            for action in self.menu_reference[actions]:
                action.triggered.connect(self.MenuEvent)

    
    def init_toolBar(self, status):
       if status:
           for i, action in enumerate(self.ToolBarActions):
               self.ToolBarActions[action].triggered.connect(lambda _, index=i: self.LayoutStack.setCurrentIndex(index))


    def MenuEvent(self):
        sender = self.sender()

        if sender.text() == "Exit":
            sys.exit(0)
        elif sender.text() == "Dark Theme":

            self.setStyleSheet(load_style("assests/mainWindow/themes/MainWindow.qss"))
            self.DataViewer.setStyleSheet(load_style("assests/Data_viewer/Themes/dataViwereStyle.qss"))
            self.Visualization.setStyleSheet(load_style("assests/visualization/themes/visualizationLight.qss"))
            self.Report.setStyleSheet(load_style("assests/Report/theme/report.qss"))

        elif sender.text() == "Light Theme":

            self.setStyleSheet(load_style("assests/mainWindow/themes/lightMainWindow.qss"))
            self.DataViewer.setStyleSheet(load_style("assests/Data_viewer/Themes/lightdataviwereStyle.qss"))
            self.Visualization.setStyleSheet(load_style("assests/visualization/themes/lightvisualization.qss"))
            self.Report.setStyleSheet(load_style("assests/Report/theme/lightreport.qss"))
            
        else:
            path = os.path.expanduser("~/Quick access")
                
            file_path = self.file_dialog(sender.text(), path)

            if file_path:
                self.reset_davin()
                self.DataViewer.HandleDrop(file_path)
            else:
                show_message(self, "No file selected....")

    def file_dialog(self, file_type: str, path: str):

        if file_type == "CSV File":
            file_path,_ = QFileDialog.getOpenFileName(self, "Select File", path, "File (*.csv)")
        else:
            file_path,_ = QFileDialog.getOpenFileName(self, "Select File", path, "File (*.xlsx)")

        return file_path
    


    def reset_davin(self):
        self.Visualization.fig = None
        self.Visualization.Selected_X = None
        self.Visualization.Selected_Y = None
        self.Visualization.chart_place_holder.screen.start()
        self.Visualization.Xlable.clear()
        self.Visualization.Ylable.clear()
        self.Visualization.chart_Title.clear()
        self.Visualization.visualization_count = 0

        self.DataViewer.numeric_column_list.clear()
        self.DataViewer.categorical_columns_list.clear()

        self.Visualization.NumericList.clear()
        self.Visualization.charList.clear()

        self.Visualization.UserSavedCharts.clear()

        self.Report.Selected_Chart = None
        self.Report.saved_chart.clear()

        self.setTempDir()
        
        self.Visualization.chartStack.setCurrentIndex(0)

    def setTempDir(self):
            path = "Temp/visualizations"

            if os.path.exists(path):
                shutil.rmtree(path)
            
            os.makedirs(path)


    def closeEvent(self, event):
        conformation = QMessageBox.question(self, "Exit", "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if conformation == QMessageBox.Yes:
            shutil.rmtree("Temp/visualizations")
            event.accept()
        else:
            event.ignore()




if __name__ == "__main__":
    app = QApplication([])

    splash_screen = SplashScreen()
    splash_screen.show()

    initDavin = init_davin()

    initDavin.current_state.connect(splash_screen.Update_Current_Process)
    initDavin.finished_setup.connect(initDavin.quit)

    def display_davin():
        initDavin.deleteLater()
        davin = Davin_Core()
        splash_screen.hide()

        davin.show()
        app.main_window = davin

    initDavin.finished.connect(display_davin)
    QTimer.singleShot(0, initDavin.start)

    app.exec_()

    


    
 



    


