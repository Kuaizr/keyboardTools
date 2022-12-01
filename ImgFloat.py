from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import sys

class ImgFloat(QWidget):
    close = pyqtSignal(str)
    mousepress = False
    def __init__(self,x,y,w,h,imgpath):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.imgpath = imgpath
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.maxw = 2*w
        self.maxh = 2*h
        self.minw = int(0.5*w)
        self.minh = int(0.5*h)
        self.tempx = 0
        self.tempy = 0
        self.setMouseTracking(True)
        self.setImg()

    def setImg(self):
        self.setGeometry(QRect(self.x, self.y, self.w, self.h))
        self.img = QLabel(self)
        self.img.setPixmap(QPixmap(self.imgpath))
        self.img.setScaledContents(True)
        self.img.setStyleSheet('background-color: rgb(255, 255, 255);')
        self.img.setGeometry(QRect(0, 0,self.w, self.h))
        self.img.show()

    def wheelEvent(self, event):
        angle=event.angleDelta() / 8
        angleY=angle.y() # 竖直滚过的距离
        if angleY > 0:
            w = int(1.1 * self.w)
            h = int(1.1 * self.h)
            self.w = w if w <= self.maxw else self.maxw
            self.h = h if h <= self.maxh else self.maxh
            self.setImg()
        else: # 滚轮下滚
            w = int(0.9 * self.w)
            h = int(0.9 * self.h)
            self.w = w if w >= self.minw else self.minw
            self.h = h if h >= self.minh else self.minh
            self.setImg()

    def mousePressEvent(self, event):
        key_name = event.button()
        if key_name == 1:
            self.mousepress = True
            self.tempx = event.x()
            self.tempy = event.y()
        elif key_name == 2:
            self.close.emit(self.imgpath)
        

    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()
        if self.mousepress:
            self.x = x - self.tempx + self.x
            self.y = y - self.tempy + self.y
            self.setGeometry(QRect(self.x, self.y, self.w, self.h))
 
    def mouseReleaseEvent(self, event):
        key_name = event.button()
        if key_name == 1:
            self.mousepress = False

# if __name__ == '__main__':
#     application=QApplication(sys.argv)#窗口通讯
#     root=ImgFloat(100,100,400,400)#创建对象
#     root.show()#展示窗口
#     sys.exit(application.exec_())