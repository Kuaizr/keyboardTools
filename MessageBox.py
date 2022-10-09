import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from torch import import_ir_module
from ListenKeyBoard import ListenKeyBoard
from GIF import GIF
 
class MessageBox(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.labeltitle = QLabel(self)
        self.label = QLabel(self)
        self.labelinfo = QLabel(self)

        self.labeltitle.setIndent(2)
        self.labeltitle.setAlignment(Qt.AlignLeft)
        self.label.setAlignment(Qt.AlignCenter)
        self.labelinfo.setAlignment(Qt.AlignCenter)
        self.labelinfo.setWordWrap(True)
        self.labelinfo.adjustSize()

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.labeltitle)
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.labelinfo)
        self.setLayout(self.vbox)


        self.keyboard = ListenKeyBoard()
        self.keyboard.signal.connect(self.getemit)
        self.keyboard.gif.connect(self.getgif)

        self.gif = GIF()


        self.keyboard.start()

    def getgif(self,temp):
        if temp == "begin":
            print(1)
            self.gif.begingif()
            # self.gif.signal.connect(self.getemit)
        elif temp == "end":
            print("********************************************************************************************************************")
            self.gif.endgif()

    def getemit(self,temp):
        self.setInfo(temp[0],temp[1])
    
    def setInfo(self,title,info):
        self.labeltitle.setText("<font color=\"#56adbc\" size = \"24\"><b>" + title + "</b></font>")
        self.label.setText("<font color=\"#56adbc\"><b>-----------------------------------------</b></font>")
        self.labelinfo.setText("<font color=\"#56adbc\" size = \"18\"><b>" + info + "</b></font>")
        # self.setFocusPolicy()
        QTimer.singleShot(3000, self.cleanInfo)
    
    def cleanInfo(self):
        self.labeltitle.setText("")
        self.label.setText("")
        self.labelinfo.setText("")





if __name__ == '__main__':
    application=QApplication(sys.argv)#窗口通讯
    root=MessageBox()#创建对象
    root.resize(230,100)
    root.show()#展示窗口
    sys.exit(application.exec_())
