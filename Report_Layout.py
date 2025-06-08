from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QStackedLayout, QTextEdit, 
                             QPushButton, QSpacerItem, QSizePolicy, QFontComboBox, QComboBox, QToolButton,
                             QButtonGroup)
from PyQt5.QtGui import QIcon
from util import Animation_Lable, load_style, resource_path

class ReportLayout(QWidget):

    def __init__(self):
        super().__init__()

        self.report_mainLayout = QVBoxLayout()

        self.text_tools = QHBoxLayout()

        self.report_body = QHBoxLayout()
        self.report_footer = QHBoxLayout()

        self.report_wrapper = QVBoxLayout()

        self.tools = QWidget()
        self.tools_container = QVBoxLayout()

        self.tools.setLayout(self.tools_container)
        

        self.report_container = QWidget()
        self.ReportStack = QStackedLayout()
        self.report_container.setLayout(self.ReportStack)


        self.report_place_holder = Animation_Lable(resource_path("assests/mainWindow/UI_GIF/ReportAnimation.gif"))
        self.saved_chart = QListWidget()
        self.text_area = QTextEdit()

        self.text_area.setPlaceholderText("Write Your Report.....")

        self.report_save_btn = QPushButton("Save") 


        # ---- tools
        self.alignGroup = QButtonGroup()
        self.pointGroup = QButtonGroup()

        self.fonts = QFontComboBox()
        self.fontSize = QComboBox()

        self.bold_btn = QToolButton()
        self.bold_btn.setToolTip("Bold")
        self.bold_btn.setText("B")

        self.italic_btn = QToolButton()
        self.italic_btn.setToolTip("Italic")
        self.italic_btn.setText("𝐼")

        self.underline_btn = QToolButton()
        self.underline_btn.setToolTip("Underline")
        self.underline_btn.setText("U̲")

        self.moreOptions_btn = QToolButton()
        self.moreOptions_btn.setToolTip("More")
        self.moreOptions_btn.setIcon(QIcon(resource_path("assests/Report/buttons/menu.png")))

        self.centerAlign = QToolButton()
        self.centerAlign.setToolTip("Align Center")
        self.centerAlign.setIcon(QIcon(resource_path("assests/Report/buttons/center-align.png")))

        self.leftAlign = QToolButton()
        self.leftAlign.setToolTip("Align Left")
        self.leftAlign.setIcon(QIcon(resource_path("assests/Report/buttons/left-align.png")))

        self.rightAlign = QToolButton()
        self.rightAlign.setToolTip("Align Right")
        self.rightAlign.setIcon(QIcon(resource_path("assests/Report/buttons/Right-align.png")))

        self.justify = QToolButton()
        self.justify.setToolTip("Justify")
        self.justify.setIcon(QIcon(resource_path("assests/Report/buttons/justify.png")))

        self.bulletPoint = QToolButton()
        self.bulletPoint.setToolTip("Bullet point")
        self.bulletPoint.setIcon(QIcon(resource_path("assests/Report/buttons/list-interface-symbol.png")))

        self.numberPoint = QToolButton()
        self.numberPoint.setToolTip("Number Point")
        self.numberPoint.setIcon(QIcon(resource_path("assests/Report/buttons/point.png")))

        self.TextColor = QToolButton()
        self.TextColor.setToolTip("Text Color")
        self.TextColor.setIcon(QIcon(resource_path("assests/Report/buttons/color-text.png")))


        self.setup_body()
        self.setup_footer()

        self.setLayout(self.report_mainLayout)
        self.setStyleSheet(load_style(resource_path("assests/Report/theme/report.qss")))
        self.ReportStack.setCurrentIndex(0)
        self.report_place_holder.screen.start()


    def setup_body(self):

        self.setupTools()
        
        self.ReportStack.addWidget(self.report_place_holder)
        self.ReportStack.addWidget(self.text_area)

        self.report_wrapper.addLayout(self.text_tools)
        self.report_wrapper.addWidget(self.report_container)

        
        self.report_body.addWidget(self.saved_chart, 20)
        self.report_body.addLayout(self.report_wrapper, 80)
        self.report_body.addWidget(self.tools)

        self.tools.hide()


        self.report_mainLayout.addLayout(self.report_body)



    def setup_footer(self):
        self.report_footer.addWidget(self.report_save_btn)

        self.report_footer.addSpacerItem(QSpacerItem(40, 20,  QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.report_mainLayout.addLayout(self.report_footer)


    def setupTools(self):
        self.text_tools.addWidget(self.bold_btn)
        self.bold_btn.setCheckable(True)

        self.text_tools.addWidget(self.italic_btn)
        self.italic_btn.setCheckable(True)

        self.text_tools.addWidget(self.underline_btn)
        self.underline_btn.setCheckable(True)
        
        self.text_tools.addWidget(self.fonts)
        self.text_tools.addWidget(self.fontSize)
        self.fontSize.addItems([str(s) for s in range(8, 31, 2)])

        self.text_tools.addWidget(self.moreOptions_btn)
        self.moreOptions_btn.setCheckable(True)

        self.alignGroup.setExclusive(True)
        self.pointGroup.setExclusive(True)

        self.leftAlign.setCheckable(True)
        self.rightAlign.setCheckable(True)
        self.centerAlign.setCheckable(True)
        self.justify.setCheckable(True)
        self.bulletPoint.setCheckable(True)
        self.numberPoint.setCheckable(True)

        self.alignGroup.addButton(self.leftAlign)
        self.alignGroup.addButton(self.rightAlign)
        self.alignGroup.addButton(self.centerAlign)
        self.alignGroup.addButton(self.justify)

        self.pointGroup.addButton(self.bulletPoint)
        self.pointGroup.addButton(self.numberPoint)

        self.tools_container.addWidget(self.leftAlign)
        self.tools_container.addWidget(self.rightAlign)
        self.tools_container.addWidget(self.centerAlign)
        self.tools_container.addWidget(self.justify)
        self.tools_container.addWidget(self.bulletPoint)
        self.tools_container.addWidget(self.numberPoint)

        self.tools_container.addWidget(self.TextColor)

        






        
