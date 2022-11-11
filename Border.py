from cProfile import label
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import sys

class Border(QWidget):

    def __init__(self,x,y,w,h):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setStyleSheet('border-width: 1px;border-style: solid;border-color: red;background-color: red;')
        self.setGeometry(QRect(x,y,w,h))
        self.show()





# if __name__ == '__main__':
#     res = [100,100,600,600]
#     application=QApplication(sys.argv)#窗口通讯
#     b1=Border(100,100,1,600)#创建对象
#     b2=Border(100,100,600,1)#创建对象
#     b3=Border(700,100,1,600)#创建对象
#     b4=Border(100,700,600,1)#创建对象
#     b1.show()#展示窗口
#     b2.show()#展示窗口
#     b3.show()#展示窗口
#     b4.show()#展示窗口
#     sys.exit(application.exec_())