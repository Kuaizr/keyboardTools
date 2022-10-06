import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import time
from ImgBed import ImageBed
from clipboard import set_clipboard, get_clipboard
import keyboard
from youdao import youdao
 
class MessageBox(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowFlags(Qt.FramelessWindowHint) # 无边框
        self.setAttribute(Qt.WA_TranslucentBackground) # 全透明
        
        self.labeltitle = QLabel(self)
        self.label = QLabel(self)
        self.labelinfo = QLabel(self)

        self.labeltitle.setIndent(2)
        self.labeltitle.setAlignment(Qt.AlignLeft)
        self.label.setAlignment(Qt.AlignCenter)
        self.labelinfo.setAlignment(Qt.AlignCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.labeltitle)
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.labelinfo)

        self.setLayout(self.vbox)
        self.keyboard = WorkThread(self)
        self.keyboard.signal.connect(self.getemit)
        self.keyboard.start()

    def getemit(self,temp):
        self.setInfo(temp[0],temp[1])
    
    def setInfo(self,title,info):
        self.labeltitle.setText("<font color=\"#56adbc\" size = \"24\">" + title + "</font>")
        self.label.setText("<font color=\"#56adbc\">-----------------------------------------</font>")
        self.labelinfo.setText("<font color=\"#56adbc\" size = \"18\">" + info + "</font>")
        # self.setFocusPolicy()
        QTimer.singleShot(3000, self.cleanInfo)
    
    def cleanInfo(self):
        self.labeltitle.setText("")
        self.label.setText("")
        self.labelinfo.setText("")

class WorkThread(QThread):
    signal = pyqtSignal(list)
    def __init__(self,parent):
        super().__init__()
        self.parent = parent
        self.mark ={'value': 0}
        self.imgbed = ImageBed()
    def run(self):
        keyboard.add_hotkey('ctrl+alt', self.uploadimg ,suppress = False)
        keyboard.add_hotkey('ctrl+c', self.timimg,suppress = False)
        keyboard.wait()


    def uploadimg(self):
        result = self.imgbed.pushimg()
        if result == "no img need to upload":
            temp = ["failed",result]
            self.signal.emit(temp)
        else:
            temp = ["success!",result]
            self.signal.emit(temp)
            set_clipboard(result)

    def timimg(self):
        if self.mark['value'] == 0:
            self.mark['value'] = time.time() * 1000
        else:
            marktime = int(time.time() * 1000 - self.mark['value'])
            if marktime <= 500:
                self.mark['value'] = 0
                self.fanyi()
            else:
                self.mark['value'] = 0
                self.timimg(self.mark)

    def fanyi(self):
        word = get_clipboard()
        result = youdao(word)
        if result == "something wrong":
            temp = ["failed",result]
            self.signal.emit(temp)
        else:
            temp = ["success!",result]
            self.signal.emit(temp)



if __name__ == '__main__':
    application=QApplication(sys.argv)#窗口通讯
    root=MessageBox()#创建对象
    root.resize(230,100)
    root.show()#展示窗口
    root.setInfo("1","444444444444444444444")
    sys.exit(application.exec_())
