from Report_Layout import ReportLayout
from PyQt5.QtWidgets import QFileDialog, QColorDialog, QMenu
from PyQt5.QtCore import pyqtSignal, QThread, QRectF, QSizeF, Qt
from PyQt5.QtGui import QFont, QPdfWriter, QPainter, QImage, QTextDocument, QTextOption, QTextListFormat

from util import ReviewChart, show_message

import os   

class Genarate_Report(QThread):
    
    report_status = pyqtSignal(bool)

    def __init__(self, chart_path, save_path, report):
        super().__init__()

        self.save_path = save_path
        self.chart_path = chart_path
        self.report = report

    def mm_to_pixels(self, mm, dpi=300):
        return mm * dpi / 25.4

    def run(self):
        dpi = 300
        pdf_writer = QPdfWriter(self.save_path)
        pdf_writer.setPageSizeMM(QSizeF(210, 297))
        pdf_writer.setResolution(dpi)

        painter = QPainter(pdf_writer)

        chart = QImage(self.chart_path)

        img_rect = QRectF(self.mm_to_pixels(20, dpi), self.mm_to_pixels(20, dpi),
                              self.mm_to_pixels(170, dpi), self.mm_to_pixels(90, dpi))
        painter.drawImage(img_rect, chart)
        y_offset = self.mm_to_pixels(120, dpi)

        painter.drawImage(img_rect, chart)

        html = self.report.replace("<div", "<p style='margin:0;'").replace("</div>", "</p>")

        doc = QTextDocument()
        doc.setHtml(html)
        doc.setTextWidth(self.mm_to_pixels(170, dpi))
        doc.setDefaultTextOption(QTextOption(Qt.AlignJustify))
        

        doc.setPageSize(QSizeF(self.mm_to_pixels(170, dpi), self.mm_to_pixels(297 - 120, dpi)))

        painter.save()
        painter.translate(self.mm_to_pixels(20, dpi), y_offset)
        painter.scale(1.5, 1.5)

        doc.drawContents(painter)
        painter.restore()

        painter.end()
        self.report_status.emit(True)


class Report(ReportLayout):

    def __init__(self):
        super().__init__()

        
        self.Selected_Chart = None
        
        self.init_toolBar()
        self.initAlignmentTools()
        self.initPointTools()

        self.saved_chart.itemDoubleClicked.connect(self.displayChart)
        self.saved_chart.itemClicked.connect(self.SelectToReport)

        self.report_save_btn.clicked.connect(self.Make_report)
        self.moreOptions_btn.toggled.connect(self.tools.setVisible)
        self.TextColor.clicked.connect(self.setTextColor)

        self.saved_chart.setContextMenuPolicy(Qt.CustomContextMenu)
        self.saved_chart.customContextMenuRequested.connect(self.listItemOptions)


    def init_toolBar(self):
        self.fonts.currentFontChanged.connect(self.setFont)         # font Selector
        self.fontSize.currentTextChanged.connect(self.setFontSize)  # font size selector
        self.bold_btn.clicked.connect(self.applyBold)  # Bold
        self.italic_btn.clicked.connect(self.applyItalic)  # italic
        self.underline_btn.clicked.connect(self.applyUnderline) # underline 
        


    def Make_report(self):

        if self.Selected_Chart is not None:
            path =  os.path.join("Temp", "visualizations", self.Selected_Chart)
            path = path + ".png"
            temp_path = os.path.expanduser("~/Documents")
            save_path, _ = QFileDialog.getSaveFileName(self, "Save PDF", temp_path, "PDF Files (*.pdf)")

            if not save_path:
                show_message(self, "No save Path selected")
                return

            self.report_save_btn.setDisabled(True)
            if not self.text_area.toPlainText().strip():
                show_message(self, "Report is Empty...")
                self.report_save_btn.setDisabled(False)
                return

            self.report_save_btn.setDisabled(True)
            report_text = self.text_area.toHtml()
        
            self.process_report = Genarate_Report(path,save_path,report_text)
            self.process_report.report_status.connect(self.showReportStatus)
            self.process_report.start()
            
        

    
    def getSavedChart(self, chart):
        self.saved_chart.addItem(chart)

    
    def displayChart(self, item):
        path = "Temp\\visualizations"
        chart = item.text()
        chart = chart + ".png"
        path = os.path.join(path, chart)

        self.chart_body = ReviewChart(path)

        self.chart_body.exec_()

    def SelectToReport(self, item):
        self.Selected_Chart = item.text()
        self.ReportStack.setCurrentIndex(1)


    def setFont(self, font):
        self.merge_format(lambda fmt: fmt.setFont(font))

    def setFontSize(self, size):
        self.merge_format(lambda fmt: fmt.setFontPointSize(float(size)))

    def applyBold(self):
        _format = self.text_area.currentCharFormat()
        _format.setFontWeight(QFont.Bold if self.bold_btn.isChecked() else QFont.Normal)
        self.text_area.setCurrentCharFormat(_format)

    def applyItalic(self):
        fmt = self.text_area.currentCharFormat()
        fmt.setFontItalic(self.italic_btn.isChecked())
        self.text_area.setCurrentCharFormat(fmt)

    def applyUnderline(self):
        fmt = self.text_area.currentCharFormat()
        fmt.setFontUnderline(self.underline_btn.isChecked())
        self.text_area.setCurrentCharFormat(fmt)

    def setTextColor(self):
        color = QColorDialog.getColor()

        if color.isValid():
            self.merge_format(lambda fmt: fmt.setForeground(color))


    def merge_format(self, func):
        cursor = self.text_area.textCursor()
        if not cursor.hasSelection():
            cursor.select(cursor.WordUnderCursor)
        fmt = cursor.charFormat()
        func(fmt)
        cursor.mergeCharFormat(fmt)
        self.text_area.mergeCurrentCharFormat(fmt)

    def initAlignmentTools(self):
        self.leftAlign.clicked.connect(lambda: self.text_area.setAlignment(Qt.AlignmentFlag.AlignLeft))
        self.rightAlign.clicked.connect(lambda: self.text_area.setAlignment(Qt.AlignmentFlag.AlignRight))
        self.centerAlign.clicked.connect(lambda: self.text_area.setAlignment(Qt.AlignmentFlag.AlignCenter))
        self.justify.clicked.connect(lambda: self.text_area.setAlignment(Qt.AlignmentFlag.AlignJustify))

    def initPointTools(self):
        self.bulletPoint.clicked.connect(lambda: self.set_list_style(QTextListFormat.ListDisc))
        self.numberPoint.clicked.connect(lambda: self.set_list_style(QTextListFormat.ListDecimal))

    def set_list_style(self, style):
        cursor = self.text_area.textCursor()
        cursor.beginEditBlock()
        list_format = QTextListFormat()
        list_format.setStyle(style)
        cursor.createList(list_format)
        cursor.endEditBlock()

    
    def showReportStatus(self, status):
        if status:
            self.report_save_btn.setDisabled(False)
            show_message(self, "Report generated and saved.")

    
    def listItemOptions(self, event):

        item = self.saved_chart.itemAt(event)

        if item is None:
            return
        
        clicked_chart = item.text()
        options = ["Delete", "View"]
        menu = QMenu()
        
        actions = {}

        for option in options:
            actions[option] = menu.addAction(option)
        
        pos = self.saved_chart.viewport().mapToGlobal(event)
        action = menu.exec_(pos)

        if action == actions["Delete"]:
            row = self.saved_chart.row(item)
            self.saved_chart.takeItem(row)
            os.remove(f"Temp/visualizations/{clicked_chart}.png")
        elif action == actions["View"]:
            self.displayChart(item)

            
        

