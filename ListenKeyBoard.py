import time
from ImgBed import ImageBed
from clipboard import set_clipboard, get_clipboard
import keyboard
from youdao import youdao
from PyQt5.QtCore import *


class ListenKeyBoard(QThread):
    signal = pyqtSignal(list)
    gif = pyqtSignal(str)
    hasgif = False
    def __init__(self):
        super().__init__()
        self.mark ={'value': 0}
        self.imgbed = ImageBed()
    def run(self):
        keyboard.add_hotkey('ctrl+alt', self.uploadimg ,suppress = False)
        keyboard.add_hotkey('ctrl+c', self.timimg,suppress = False)
        keyboard.add_hotkey('ctrl+shift+[', self.gifbegin,suppress = False)
        keyboard.add_hotkey('ctrl+shift+]', self.gifend,suppress = False)
        keyboard.wait()

    def gifbegin(self):
        if self.hasgif == False:
            self.gif.emit("begin")
            self.hasgif = True

    def gifend(self):
        print(2)
        if self.hasgif:
            self.gif.emit("end")
            self.hasgif = False

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