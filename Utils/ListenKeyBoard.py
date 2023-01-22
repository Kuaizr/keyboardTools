import time
from Utils.clipboard import get_clipboard
import keyboard
from Utils.youdao import youdao
from PyQt5.QtCore import *


class ListenKeyBoard(QThread):
    signal = pyqtSignal(list)

    gif = pyqtSignal(str)
    hasgif = False

    screen = pyqtSignal(str)
    hasScreen = False

    hasRecord = False
    record = pyqtSignal(str)

    esc = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.mark ={'value': 0}
        
    def run(self):
        keyboard.add_hotkey('ctrl+c', self.timimg,suppress = False)
        keyboard.add_hotkey('ctrl+shift+[', self.gifbegin,suppress = False)
        keyboard.add_hotkey('ctrl+shift+]', self.gifend,suppress = False)
        keyboard.add_hotkey('ctrl+shift+a', self.screencut,suppress = False)
        keyboard.add_hotkey('ctrl+shift+/', self.imgFloat,suppress = False)
        keyboard.add_hotkey('ctrl+shift+t', self.recordfunc,suppress = False)
        keyboard.add_hotkey('esc', self.escfun,suppress = False)
        keyboard.wait()
    
    def recordfunc(self):
        if self.hasRecord == False:
            self.hasRecord = True
            self.record.emit("begin")
        else:
            self.hasRecord = False
            self.record.emit("end")

    
    def imgFloat(self):
        if self.hasScreen == False:
            pass
        elif self.hasScreen == True:
            self.hasScreen = False
            self.screen.emit("imgfloat")

    def escfun(self):
        # 界面杀掉
        # 停止录屏并删除照片
        if self.hasScreen or self.hasgif:
            self.esc.emit(True)
            self.hasgif = False
            self.hasScreen = False

    def screencut(self):
        if self.hasScreen == False and self.hasgif == False:
            self.hasScreen = True
            self.screen.emit("begin")
        elif self.hasScreen == True:
            self.hasScreen = False
            self.screen.emit("end")

    def gifbegin(self):
        self.hasScreen = False
        if self.hasgif == False:
            self.gif.emit("begin")
            self.hasgif = True

    def gifend(self):
        if self.hasgif:
            self.gif.emit("end")
            self.hasgif = False


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
                self.timimg()

    def fanyi(self):
        word = get_clipboard()
        if word:
            result = youdao(word)
            if result == "something wrong":
                temp = ["failed",result]
                self.signal.emit(temp)
            else:
                temp = ["success!",result]
                self.signal.emit(temp)
        else:
            temp = ["failed","编码不支持"]
            self.signal.emit(temp)