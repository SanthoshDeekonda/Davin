from PyQt5.QtWidgets import QColorDialog, QFileDialog, QApplication
from PyQt5.QtCore import QThread, pyqtSignal, QUrl, Qt
from Visualization_layout import VisualizationLayout

from util import Generate_graph, show_message
import os

class Download_Image(QThread):

    notify_status = pyqtSignal(str)

    def __init__(self, graph, path):
        super().__init__()

        self.graph = graph
        self.path = path

        self.graph.update_layout(
            plot_bgcolor="#ffffff",
            paper_bgcolor="#ffffff",
            font=dict(color="#000000")
        )

    def run(self):
        self.notify_status.emit("started")
        try:
            self.graph.write_image(self.path, format="png")
        except Exception as e:
            self.notify_status.emit("Error")
            return
        self.notify_status.emit("ended")


class Visualization(VisualizationLayout):

    saved_visualization = pyqtSignal(str)

    def __init__(self, Data):
        super().__init__()

        self.Visualization_Data = Data
        self.UserSavedCharts = []

        self.Selected_X = None
        self.Selected_Y = None
        self.color = "#03A9F4"
        self.fig = None
        self.visualization_count = 0
        self.CurrentSavedChart = None
        
        self.save_thread = None
        self.dow_thread = None

        self.generating_chart = False


        self.Xlable.dropLable.connect(self.getXcolumn)
        self.Ylable.dropLable.connect(self.getYcolumn)

        self.Canvas.loadFinished.connect(self.show_chart)



        # ----- Button Connector
        self.color_picker_btn.clicked.connect(self.Color_Picker)
        self.clear_btn.clicked.connect(self.clear_canvas)
        self.download_btn.clicked.connect(self.download_graph)
        self.save_btn.clicked.connect(self.save_graph)

        self.chartType.itemDoubleClicked.connect(self.selected_chart)


        self.setupWebEngine()
    
    def getXcolumn(self, x_lable):
        self.Selected_X = self.Visualization_Data[x_lable]

        if self.Selected_Y is not None:
            title = self.chart_Title.text() if self.chart_Title.text() else " "
            self.create_chart(title,self.Selected_X, self.Selected_Y,self.color)

    

    def getYcolumn(self, y_lable):
        self.Selected_Y = self.Visualization_Data[y_lable]

        if self.Selected_X is not None:
            title = self.chart_Title.text() if self.chart_Title.text() else " "
            self.create_chart(title,self.Selected_X, self.Selected_Y,self.color)

           


    def getData(self, data):
        self.Visualization_Data = data

    
    def getColumnItems(self, columns: dict):
        if self.NumericList.count() > 0 and self.charList.count() > 0:
            self.NumericList.clear()
            self.charList.clear()
        
        self.NumericList.addItems(columns["numeric"])
        self.charList.addItems(columns["char"])

    
    def create_chart(self, title, x, y, color, chart_type="Bar Chart"):
        
        self.generating_chart = True
        QApplication.setOverrideCursor(Qt.WaitCursor)

        self.thread = QThread()
        self.generate_chart = Generate_graph(x,y, title, color, chart_type)
        self.generate_chart.moveToThread(self.thread)

        self.thread.started.connect(self.generate_chart.process_data)
        self.generate_chart.processed_graph.connect(self.display_chart)
        
        self.generate_chart.processed_graph.connect(self.thread.quit)

        self.thread.finished.connect(self.unlock_slot)

        self.chart_place_holder.screen.stop()
        self.graph_loading_screen.screen.start()
        self.chartStack.setCurrentIndex(2)

        self.thread.start()
        

    def display_chart(self, chart, fig):
        self.fig = fig
        self.Canvas.setHtml(chart)


    def selected_chart(self, item):

        if self.generating_chart:
            show_message(self, "Chart generation is already in progress. Please wait...")
            return

        chartType = item.text()
        if self.Selected_X is not None and self.Selected_Y is not None:
            title = self.chart_Title.text() if self.chart_Title.text() else chartType
            self.create_chart(title,self.Selected_X, self.Selected_Y, self.color, chartType)

    def unlock_slot(self):
        self.thread.deleteLater()
        self.generate_chart.deleteLater()
        QApplication.restoreOverrideCursor()
        self.generating_chart = False


    def Color_Picker(self):
        _color = QColorDialog.getColor()

        if _color.isValid():
            self.color = _color.name()


    def show_chart(self, status):
        if status:
            self.chartStack.setCurrentIndex(1)
            self.graph_loading_screen.screen.stop()

    def clear_canvas(self):
        self.chart_place_holder.screen.start()
        self.chartStack.setCurrentIndex(0)

        self.Selected_X = None
        self.Selected_Y = None
        self.fig = None

        self.Xlable.clear()
        self.Ylable.clear()
        self.chart_Title.clear()

        self.color = "#03A9F4"


    def download_graph(self):
        if self.fig is not None:
            path = os.path.expanduser("~/Documents")
            
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", path, "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;All Files (*)")

            if file_path:

                if self.dow_thread is not None and self.dow_thread.isRunning():
                    show_message(self, "Download is already in progress. Please wait...")
                    return
                
                self.dow_thread = Download_Image(self.fig, file_path)
                self.dow_thread.notify_status.connect(self.notify_dow_status)
                self.dow_thread.finished.connect(self.dow_thread.deleteLater)
                self.dow_thread.finished.connect(lambda: setattr(self, "dow_thread", None))
                self.dow_thread.start()
            else:
                show_message(self, "no file path selected....")

    def save_graph(self):
        if self.fig is not None:
            self.visualization_count += 1
            title = self.chart_Title.text() if self.chart_Title.text() else f"visualization{self.visualization_count}"
            title = " ".join(title.split())

            if title in self.UserSavedCharts:
                show_message(self, f"Visualization with {title} already exsist")
                return

            if self.save_thread is not None and self.save_thread.isRunning():
                show_message(self, "Save is already in progress. Please wait...")
                return

            self.CurrentSavedChart = title
            try:
                self.save_thread = Download_Image(self.fig, f"Temp/visualizations/{title}.png")
            except Exception as e:
                show_message("Don't use '/' and '\\' in the title.." )
            self.save_thread.notify_status.connect(self.notify_save_status)
            self.save_thread.finished.connect(self.save_thread.deleteLater)
            self.save_thread.finished.connect(lambda: setattr(self, "save_thread", None))
            self.UserSavedCharts.append(self.CurrentSavedChart)
            self.save_thread.start()
                


    def notify_dow_status(self, status):
        if status == "started":
            self.download_btn.setDisabled(True)
            show_message(self, "Exporting visualization...")
        elif status == "ended":
            self.download_btn.setDisabled(False)
            show_message(self, "Visualization successfully saved...")
        

    def notify_save_status(self, status):
        if status == "started":
            self.save_btn.setDisabled(True)
            show_message(self, "Exporting for Report....")
        elif status == "ended":
            self.saved_visualization.emit(self.CurrentSavedChart)
            self.save_btn.setDisabled(False)
            show_message(self, "Visualization ready for report...")
        elif status == "Error":
            self.save_btn.setDisabled(False)
            show_message(self, "Invlid Title")

            
    def GetSaveStatus(self, status):
        if status:
            self.saved_visualization.emit(self.CurrentSavedChart)

    
    def setupWebEngine(self):
        local_path = os.path.abspath("assests/visualization/placeHoder_html/place_holder_html.html")
        dummy_place_holder = QUrl.fromLocalFile(local_path)

        self.Canvas.load(dummy_place_holder)
        
        
    