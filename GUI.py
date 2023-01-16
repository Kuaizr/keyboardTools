import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from clipboard import set_clipboard, getImgLableBybase64

from ListenKeyBoard import ListenKeyBoard
from GIF import GIF
from ScreenTemp import ScreenTemp
from Border import Border
from UDP import UDP
from ImgFloat import ImgFloat
 
class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.udp = UDP()
        self.ifMessage = True
        self.imgbase64 = False

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

        self.imgList = dict()

        self.sysIcon = QIcon('/home/kzer/code/keyboardTools/icon_normal.png')
        self.badIcon = QIcon('/home/kzer/code/keyboardTools/icon_bad.png')
        self.setWindowIcon(self.sysIcon)
        self.createTrayIcon()

        self.keyboard.start()

    def createTrayIcon(self):
        self.changeImgType = QAction('base64?:'+str(self.imgbase64), self, triggered = self.changeImgbase64)
        self.changeUDP = QAction('showMessage?:'+str(self.ifMessage), self, triggered = self.changeifMessage)
        aQuit = QAction('Quit(&Q)', self, triggered = QApplication.instance().quit)
        
        menu = QMenu(self)
        menu.addAction(self.changeImgType)
        menu.addAction(self.changeUDP)
        menu.addAction(aQuit)
        
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(self.sysIcon)
        self.trayIcon.setContextMenu(menu)
        self.trayIcon.show()

    def changeImgbase64(self):
        self.imgbase64 = not self.imgbase64
        self.changeImgType.setText('base64?:'+str(self.imgbase64))
    
    def changeifMessage(self):
        self.ifMessage = not self.ifMessage
        self.changeUDP.setText('showMessage?:'+str(self.ifMessage))

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
        elif temp == "imgfloat":
            if self.isScreenCutBegin == True:
                self.isScreenCutBegin = False
                position =  self.screenTemp.getPosition()
                self.screenTemp.close()
                path = self.gif.screencut(position[0],position[1],position[2],position[3])
                self.imgList[path] = ImgFloat(position[0],position[1],position[2],position[3],path)
                self.imgList[path].show()
                self.imgList[path].close.connect(self.stopImgFloat)

    def stopImgFloat(self,temp):
        path = str(temp)
        del self.imgList[path]
        
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
        if self.ifMessage:
            self.showMessage(temp[0],temp[1])
        if temp[0] == "success!":
            if self.imgbase64:
                res = getImgLableBybase64(temp[1])
                set_clipboard(res)
            else:
                set_clipboard(temp[1])


    def showMessage(self,title,info):
        icon = self.sysIcon
        if title != "success!":            #根据消息类型获取图标
            icon = self.badIcon
        self.trayIcon.showMessage(title,    #标题
                                  info,     #信息
                                  icon,     #图标
                                  2000)     #信息显示持续时间
    

if __name__ == '__main__':
    application=QApplication(sys.argv)#窗口通讯
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, '系统托盘', '本系统不支持托盘功能,请注释掉self.createTrayIcon()和self.showMessage(title,info),并解开其他注释')
        sys.exit(1)
        
    QApplication.setQuitOnLastWindowClosed(False)
    root=Main()#创建对象
    root.resize(230,100)
    # root.show()#展示窗口
    sys.exit(application.exec_())
