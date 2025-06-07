from PyQt5.QtWidgets import QLabel, QLineEdit, QListWidget, QDialog, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt, QMimeData, QObject, QTimer
from PyQt5.QtGui import QPainter, QDrag, QPixmap, QColor, QMovie

import plotly.graph_objects as go

import os
import pandas as pd
import numpy as np




class DropLable(QLabel):

    DropSignal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        
        self.setAcceptDrops(True)
        

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.DropSignal.emit(file_path)
        else:
            self.setText("Invalid file")

        
    

class DropLineEdit(QLineEdit):
    dropLable = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        data = event.mimeData().text().strip()
        self.setText(data)
        self.dropLable.emit(data)




class DraggableListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setDragEnabled(True)

    def startDrag(self, supportedActions):
        item = self.currentItem()
        if not item:
            return

        mimeData = QMimeData()
        mimeData.setText(item.text())


        drag = QDrag(self)
        drag.setMimeData(mimeData)

        
        pixmap = QPixmap(120, 30)
        pixmap.fill(Qt.transparent)

        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        
        painter.setBrush(QColor("#555"))
        painter.setPen(Qt.NoPen)  
        painter.drawRoundedRect(pixmap.rect(), 5, 5) 

        
        font = painter.font()
        font.setBold(True)
        font.setPointSize(10)  
        painter.setFont(font)

        
        painter.setPen(Qt.white)

        painter.drawText(pixmap.rect(), Qt.AlignCenter, item.text())

        painter.end()

        drag.setPixmap(pixmap)
        drag.setHotSpot(pixmap.rect().center())

        drag.exec_(Qt.CopyAction)




class Generate_graph(QObject):

    processed_columns = pyqtSignal(np.ndarray, np.ndarray, str)
    processed_graph = pyqtSignal(str, object)
    error_message = pyqtSignal(str)

    def __init__(self, x_data, y_data, title, color, chart_type="bar"):
        super().__init__()


        self.x_data = x_data
        self.y_data = y_data

        self.chart_type = chart_type
        self.color = color
        self.title = title
        self.x_label = self.x_data.name
        self.y_label = self.y_data.name

        self.processed_columns.connect(self.generate_chart)


    def process_data(self):
        df = pd.DataFrame({
            'x': self.x_data,
            'y': self.y_data
        })

        x_is_cat = not pd.api.types.is_numeric_dtype(self.x_data)
        y_is_cat = not pd.api.types.is_numeric_dtype(self.y_data)

        if x_is_cat and not y_is_cat:
            df = df.drop_duplicates(subset='x')
        elif y_is_cat and not x_is_cat:
            df = df.drop_duplicates(subset='y')
        elif x_is_cat and y_is_cat:
            df = df.drop_duplicates()


        filtered_x = df['x'].to_numpy()
        filtered_y = df['y'].to_numpy()

        self.processed_columns.emit(filtered_x, filtered_y, self.chart_type)

    def generate_chart(self, x, y, chart_type):
        chart_generator = {
            "Bar Chart": lambda: go.Figure(data=[go.Bar(x=x, y=y, marker_color=self.color)]),
            "Horizontal Bar Chart": lambda:  go.Figure(data=[go.Bar(x=y, y=x, orientation='h', marker_color=self.color)]),
            "Line Plot": lambda: go.Figure(data=[go.Scatter(x=x, y=y, mode='lines+markers', line=dict(color=self.color))]),
            "Pie Chart": lambda: go.Figure(data=[go.Pie(labels=x, values=y)]),
            "Scatter Plot": lambda: go.Figure(data=[go.Scatter(x=x, y=y, mode='markers', line=dict(color=self.color))]),
            "Histogram": lambda: go.Figure(data=[go.Histogram(x=x, marker_color=self.color)]),
            "Area Chart": lambda: go.Figure(data=[go.Scatter(x=x, y=y, fill='tozeroy', mode='lines', line=dict(color=self.color))]),
            "Box Plot": lambda: go.Figure(data=[go.Box(y=y, name=self.title, marker_color=self.color)]),
            "Donut Chart": lambda: go.Figure(data=[go.Pie(labels=x, values=y, hole=0.4)]),
            "Bubble Chart": lambda: go.Figure(data=[go.Scatter(x=x, y=y, mode='markers',
                                    marker=dict(
                                        size=y,
                                        color=self.color,
                                        sizemode='area',
                                        sizeref=2.*max(y)/(40.**2),
                                        sizemin=4
                                    ))]),
            "Treemap": lambda: go.Figure(data=[go.Treemap(labels=x, parents=[""] * len(x),values=y )]),
            "Radar Chart": lambda: go.Figure(data=[go.Scatterpolar(r=y, theta=x, fill='toself', line=dict(color=self.color))]),
            "Waterfall": lambda: go.Figure(data=[go.Waterfall(x=x, y=y, connector={"line":{"color":"rgb(63, 63, 63)"}})])            

        }

        try:
            fig = chart_generator.get(chart_type, lambda: go.Figure())()
        except Exception as e:
            self.error_message.emit(f"Error generating chart")
            return

        if chart_type == "Histogram":
            fig.update_layout(
                title=self.title,
                xaxis_title=self.x_label,
                bargap=0.1,
            )

        elif chart_type == "Radar Chart":
            fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=False,
                                title=self.title,
                                xaxis_title=self.x_label,
                                yaxis_title=self.y_label,
                                plot_bgcolor="#333",
                                paper_bgcolor="#333",
                                font=dict(color="white")
                              )
        else:
            fig.update_layout(
                title=self.title,
                xaxis_title=self.x_label,
                yaxis_title=self.y_label,
                plot_bgcolor="#333",
                paper_bgcolor="#333",
                font=dict(color="white"),
            )
            
        config = {
                "modeBarButtonsToRemove": ["lasso2d", "toImage"],
                "displaylogo": False
            }
        chart_html = fig.to_html(include_plotlyjs='cdn', config=config)

        self.processed_graph.emit(chart_html, fig)



class Animation_Lable(QLabel):
    def __init__(self, Animation_path):
        super().__init__()
        self.path = Animation_path
        self.setText("Loading....")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.screen = QMovie(self.path)

        if self.screen.isValid():
            self.setMovie(self.screen)

class ReviewChart(QDialog):

    def __init__(self, chart_path):
        super().__init__()

        self.Layout = QHBoxLayout()
        self.setWindowTitle("Visualization preview")

        self.chart_holder = QLabel()
        self.chartImg = QPixmap(chart_path)

        self.chart_holder.setPixmap(self.chartImg)

        self.Layout.addWidget(self.chart_holder)

        self.setLayout(self.Layout)


def show_message(self, message):
    toast = QLabel(message, self)
    toast.setStyleSheet("""
        background-color: #323232;
        color: white;
        padding: 10px;
        border-radius: 10px;
        font-size: 13px;
    """)
    toast.setAlignment(Qt.AlignCenter)
    toast.setWindowFlags(Qt.ToolTip)
    toast.adjustSize()

    x = (self.width() - toast.width()) // 2
    y = (self.height() - toast.height()) // 2
    toast.move(x, y)

    toast.show()
    QTimer.singleShot(2000, toast.close)

def load_style(path: str):
    with open(path, "r") as stylesheet:
        return stylesheet.read()
    
def checkFileFormat(file: str) -> str:
    _,ext = os.path.splitext(file)
    return ext
 
