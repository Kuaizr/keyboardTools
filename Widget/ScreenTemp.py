from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import sys

class ScreenTemp(QWidget):
    position = [0,0,0,0]
    mousepress = False
    labelmove = False
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.showFullScreen()
        self.setWindowOpacity(0.3)

        self.desktop =  QApplication.desktop()
        self.x = 0
        self.y = 0
        self.endx = self.desktop.width()
        self.endy = self.desktop.height()
        self.tempx = 0
        self.tempy = 0
        self.position = [self.x ,self.y ,self.endx - self.x ,self.endy - self.y]
        self.setMouseTracking(True)
        

        self.mask = QLabel(self)
        self.mask.installEventFilter(self)
        self.mask.setGeometry(QRect(0, 0, 0, 0))
        self.mask.setFrameShape(QFrame.Box)
        self.mask.setFrameShadow(QFrame.Raised)
        self.mask.setFrameShape(QFrame.Box)
        self.mask.setStyleSheet('border-width: 1px;border-style: solid;border-color: rgb(255, 170, 0);background-color: rgb(100, 149, 237);')

        self.mask.show()

    def eventFilter(self, obj, event):
        if event.type() == 10:
            # 鼠标移入截图框
            self.labelmove = True
            return True
        elif event.type() == 11: 
            # 鼠标移出截图框
            self.labelmove = False
            return True
        return False

    def mousePressEvent(self, event):
        key_name = event.button()
        if key_name == 1:
            self.mousepress = True
            x = event.x()
            y = event.y()
            if self.labelmove == False:
                self.x = x
                self.y = y
                self.endx = x - self.x
                self.endy = y - self.y
                self.mask.setGeometry(QRect(self.x, self.y, self.endx, self.endy))
            else:
                self.tempx = x - self.x
                self.tempy = y - self.y
        elif key_name == 2:
            self.mousepress = True
            self.labelmove == False
            x = event.x()
            y = event.y()
            self.endx = x - self.x
            self.endy = y - self.y
            self.mask.setGeometry(QRect(self.x, self.y, self.endx, self.endy))

    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()
        if self.mousepress and self.labelmove == False:
            self.endx = x - self.x
            self.endy = y - self.y
            self.mask.setGeometry(QRect(self.x, self.y, self.endx, self.endy))
            self.position =  self.caculatePositon()
        elif self.mousepress and self.labelmove:
            self.x = x - self.tempx
            self.y = y - self.tempy
            self.mask.setGeometry(QRect(self.x, self.y, self.endx, self.endy))
            self.position =  self.caculatePositon()
 
    def mouseReleaseEvent(self, event):
        key_name = event.button()
        if key_name == 1:
            self.mousepress = False
            self.labelmove == False
        elif key_name == 2:
            self.mousepress = False
            self.labelmove == False
    
    def caculatePositon(self):
        desktopwidth = self.desktop.width()
        desktopheight= self.desktop.height()
        x = self.x
        y = self.y
        endx = self.endx
        endy = self.endy
        if x <= 0:
            endx = endx + x
            x = 0
        if y <= 0:
            endy = endy + y
            y = 0
        if endx + x > desktopwidth:
            endx = desktopwidth - x
        if endy + y > desktopheight:
            endy = desktopheight - y
        
        return [x,y,endx,endy]
    
    def getPosition(self):
        return self.position

