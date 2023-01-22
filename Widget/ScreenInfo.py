from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class ScreenInfo(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput | Qt.Tool)
        
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.hideInfo)

        self.desktop =  QApplication.desktop()
        self.setGeometry(0,self.desktop.height() * 0.85,self.desktop.width(),self.desktop.height() * 0.1)
        self.setMouseTracking(True)
        
        self.info = QLabel(self)
        self.info.setGeometry(0,0,self.desktop.width(),self.desktop.height() * 0.1)
        self.info.setAlignment(Qt.AlignCenter)
        self.info.setFont(QFont("Arial", 24, QFont.Black))
        self.info.setStyleSheet('border:0px')
        self.info.show()
    
    def showInfo(self,info):
        self.timer.stop()
        self.info.setText(info)
        self.show()
        self.timer.start(3000)
    
    def hideInfo(self):
        self.info.setText("")