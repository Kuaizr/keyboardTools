import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from clipboard import set_clipboard

from ListenKeyBoard import ListenKeyBoard
from GIF import GIF
from ScreenTemp import ScreenTemp
from Border import Border
 
class Main(QWidget):
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
        self.keyboard.esc.connect(self.doesc)
        self.keyboard.screen.connect(self.screen)

        self.gif = GIF()
        self.isScreenCutBegin = False
        self.isGifBegin = False
        self.gif.signal.connect(self.getemit)
        self.borderlist = []

        self.keyboard.start()


    def doesc(self,temp):
        if temp:
            if self.screenTemp and self.isScreenCutBegin and self.isGifBegin:
                self.screenTemp.close()
                self.isScreenCutBegin = False
                self.isGifBegin = False
                self.gif.endgif()
                ## 删除所有痕迹
            elif self.screenTemp and self.isScreenCutBegin and self.isGifBegin == False:
                self.screenTemp.close()
                self.isScreenCutBegin = False
                self.isGifBegin = False

    def screen(self,temp):
        if temp == "begin":
            if self.isScreenCutBegin == False:
                self.isScreenCutBegin = True
                self.screenTemp = ScreenTemp()
                self.screenTemp.show()
        elif temp == "end":
            if self.isScreenCutBegin == True:
                self.isScreenCutBegin = False
                position =  self.screenTemp.getPosition()
                self.screenTemp.close()
                self.gif.screencut(position[0],position[1],position[2],position[3])
            

    def getgif(self,temp):
        if temp == "begin":
            if self.isScreenCutBegin and self.isGifBegin == False:
                self.isGifBegin = True
                position =  self.screenTemp.getPosition()
                self.screenTemp.close()
                #self.showBorder(position)
                self.gif.begingif(position[0],position[1],position[2],position[3])
        elif temp == "end":
            if self.isScreenCutBegin and self.isGifBegin:
                self.isScreenCutBegin = False
                self.isGifBegin = False
                #self.closeBorder()
                self.gif.endgif()

    def showBorder(self,position):
        # 计算每个border的位置
        p1 = [position[0]-1,position[1],1,position[3]]
        p2 = [position[0],position[1]-1,position[2],1]
        p3 = [position[0] + position[2],position[1],1,position[3]]
        p4 = [position[0],position[1] + position[3],position[2],1]
        self.borderlist.append(Border(p1[0],p1[1],p1[2],p1[3]))
        self.borderlist.append(Border(p2[0],p2[1],p2[2],p2[3]))
        self.borderlist.append(Border(p3[0],p3[1],p3[2],p3[3]))
        self.borderlist.append(Border(p4[0],p4[1],p4[2],p4[3]))

    def closeBorder(self):
        for i in self.borderlist:
            i.close()
        self.borderlist = []

    def getemit(self,temp):
        self.setInfo(temp[0],temp[1])
        if temp[0] == "success!":
            set_clipboard(temp[1])
    
    def setInfo(self,title,info):
        self.labeltitle.setText("<font color=\"#56adbc\" size = \"24\"><b>" + title + "</b></font>")
        self.label.setText("<font color=\"#56adbc\"><b>-----------------------------------------</b></font>")
        self.labelinfo.setText("<font color=\"#56adbc\" size = \"10\"><b>" + info + "</b></font>")
        QTimer.singleShot(3000, self.cleanInfo)
    
    def cleanInfo(self):
        self.labeltitle.setText("")
        self.label.setText("")
        self.labelinfo.setText("")





if __name__ == '__main__':
    application=QApplication(sys.argv)#窗口通讯
    root=Main()#创建对象
    root.resize(230,100)
    root.show()#展示窗口
    sys.exit(application.exec_())
