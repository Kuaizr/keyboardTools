import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import subprocess

from Utils.clipboard import set_clipboard, getImgLableBybase64, getImgLableToMarkdown

from Utils.ListenKeyBoard import ListenKeyBoard
from Utils.GIF import GIF
from Widget.ScreenTemp import ScreenTemp
from Utils.UDP import UDP
from Widget.ImgFloat import ImgFloat
from Utils.Config import config
 
class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 初始化配置文件        
        if config['Translation']['enable']:
            from Utils.Translation import Translation
            self.translation = Translation()
            self.translation.text.connect(self.getemit)
        if config['UDP']['enable']:
            self.udp = UDP()
            self.udp.signal.connect(self.showMessage)

        self.ifMessage = config['ifMessage']
        self.imgType = config['imgType']

        self.keyboard = ListenKeyBoard()
        self.keyboard.signal.connect(self.getemit)
        self.keyboard.gif.connect(self.getgif)
        self.keyboard.esc.connect(self.doesc)
        self.keyboard.screen.connect(self.screen)
        self.keyboard.record.connect(self.record)

        self.gif = GIF()
        self.isScreenCutBegin = False
        self.isGifBegin = False
        self.gif.signal.connect(self.getemit)

        self.imgList = dict()

        self.sysIcon = QIcon(config['icon']['normal'])
        self.badIcon = QIcon(config['icon']['bad'])
        self.setWindowIcon(self.sysIcon)
        self.createTrayIcon()

        self.keyboard.start()

    def createTrayIcon(self):
        self.ImgTypeButton = QAction('图片格式:'+str(self.imgType), self, triggered = self.changeImgType)
        self.MessageButton = QAction('显示通知:'+str(self.ifMessage), self, triggered = self.changeifMessage)
        aQuit = QAction('退出(&Q)', self, triggered = QApplication.instance().quit)
        
        menu = QMenu(self)
        if config['UDP']['enable']:
            self.ClientButton = QAction('更改UDP客户端地址:', self, triggered = self.changeClient)
            menu.addAction(self.ClientButton)
        menu.addAction(self.ImgTypeButton)
        menu.addAction(self.MessageButton)
        menu.addAction(aQuit)
        
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(self.sysIcon)
        self.trayIcon.setContextMenu(menu)
        self.trayIcon.show()
    
    def changeClient(self):
        ipinfo,ok = QInputDialog.getText(self,"客户端地址","输入ipv4:port",text=config["UDP"]["Client"]["ipv4"]+":"+str(config["UDP"]["Client"]["port"]))
        ipv4 = config["UDP"]["Client"]["ipv4"]
        port = str(config["UDP"]["Client"]["port"])
        if ok and ipinfo:
            #验证地址合法性
            iptemp = ipinfo.split(':')
            if len(iptemp) == 2:
                ipv4 = iptemp[0]
                port = iptemp[1]
                self.udp.changeClient(ipv4,port)
            else:
                self.showMessage(["Failed!","客户端地址格式有问题，请修改"])

    def changeImgType(self):
        if self.imgType == "path":
            self.imgType = "markdown"
        elif self.imgType == "markdown":
            self.imgType = "base64"
        elif self.imgType == "base64":
            self.imgType = "path"
        self.ImgTypeButton.setText('图片格式:'+str(self.imgType))
    
    def changeifMessage(self):
        self.ifMessage = not self.ifMessage
        self.MessageButton.setText('显示通知:'+str(self.ifMessage))
    
    def record(self,temp):
        if config['Translation']['enable']:
            if temp == "begin":
                self.translation.start()
            else:
                self.translation.stop()
                self.translation.terminate()

    def doesc(self,temp):
        if temp:
            if self.screenTemp and self.isScreenCutBegin and self.isGifBegin:
                self.screenTemp.close()
                self.isScreenCutBegin = False
                self.isGifBegin = False
                ## 删除所有痕迹
                delpath = self.gif.endgif()
                delpathres = subprocess.call("del "+ delpath, shell=True)
                print(delpathres)
                if delpathres == 0:
                    print('停止录制')

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
                self.gif.begingif(position[0],position[1],position[2],position[3])
        elif temp == "end":
            if self.isScreenCutBegin and self.isGifBegin:
                self.isScreenCutBegin = False
                self.isGifBegin = False
                self.gif.endgif()

    def getemit(self,temp):
        if config['UDP']['enable']:
            self.udp.sendInfo(bytes(temp[0]+"*-*"+temp[1],'utf-8'))
        if config['ScreenInfo']['enable']:
            subprocess.run("xsetroot -name " + temp[1] ,shell=True)
        if self.ifMessage:
            self.showMessage(temp)
        if temp[0] == "success!":
            if temp[1][-3:] == "gif" or temp[1][-3:] == "png":
                if self.imgType == "path":
                    set_clipboard(temp[1])
                elif self.imgType == "markdown":
                    set_clipboard(getImgLableToMarkdown(temp[1]))
                elif self.imgType == "base64":
                    set_clipboard(getImgLableBybase64(temp[1]))
            else:
                set_clipboard(temp[1])

    def showMessage(self,temp):
        title = temp[0]
        info = temp[1]
        icon = self.sysIcon
        if title != "success!":            #根据消息类型获取图标
            icon = self.badIcon
        self.trayIcon.showMessage(title,    #标题
                                  info,     #信息
                                  icon,     #图标
                                  3000)     #信息显示持续时间

if __name__ == '__main__':
    application=QApplication(sys.argv)#窗口通讯
    if not QSystemTrayIcon.isSystemTrayAvailable():
        QMessageBox.critical(None, '系统托盘', '本系统不支持托盘功能,请注释掉self.createTrayIcon()和self.showMessage([title,info]),并解开其他注释')
        sys.exit(1)
        
    QApplication.setQuitOnLastWindowClosed(False)
    root=Main()#创建对象
    sys.exit(application.exec_())
