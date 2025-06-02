from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QApplication
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QIcon


class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setWindowTitle("Davin")
        self.setWindowIcon(QIcon("assests/mainWindow/logo/Davin_Logo.png"))
        
        self.main_Layout = QVBoxLayout()
        self.main_Layout.setContentsMargins(0,0,0,0)

        self.splashContainer = QWidget()
        self.splashLayout = QVBoxLayout(self.splashContainer)
        self.splashLayout.setContentsMargins(30,30,30,30)
        self.splashLayout.setSpacing(30)

        self.splashContainer.setObjectName("splashwidget")
        self.splashContainer.setStyleSheet("""
                #splashwidget {
                                background-color: qlineargradient(
                                spread:pad, x1:0, y1:0, x2:1, y2:1,
                                stop:0 #1f1f1f, stop:1 #2c2c2c
                            );
                                border-radius: 20px;
                                           }
        """)

        

        self.logo = QLabel()
        self.current_process_info = QLabel("Initializing...")
        
        self.SetupSplashScreen()
        self.resize(450, 320)
        self.splashContainer.resize(450, 320)
        self.setLayout(self.main_Layout)


    def SetupSplashScreen(self):

        self.logo_pixmap = QPixmap("assests/mainWindow/logo/Davin_Logo.png").scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo.setPixmap(self.logo_pixmap)
        self.logo.setAlignment(Qt.AlignCenter)

        self.current_process_info.setFont(QFont("Segoe UI", 10))
        self.current_process_info.setStyleSheet("color: #AAAAAA;")
        self.current_process_info.setAlignment(Qt.AlignCenter)

        self.splashLayout.addWidget(self.logo)
        self.splashLayout.addWidget(self.current_process_info)

        self.main_Layout.addWidget(self.splashContainer)

    def Update_Current_Process(self, process):
        self.current_process_info.setText(process)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    sys.exit(app.exec_())
