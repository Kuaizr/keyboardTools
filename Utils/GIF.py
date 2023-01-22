from Utils.Config import config
import time
import subprocess
from PyQt5.QtCore import *
 
# 屏幕录制画面大小
class GIF(QThread):
    signal = pyqtSignal(list)
    def __init__(self):
        super().__init__()

        #ffmpeg 录制视频 -> 调色板 -> gif
        #ffmpeg 截屏

    def screencut(self,offset_x = 0, offset_y = 0, width = 1920, height = 1080):
        filename = config['GIF']['filepath'] + str(int(time.time() * 1000))+".png"
        res = subprocess.call("ffmpeg -f gdigrab -s "+ str(width) +"x"+ str(height) +" -offset_x "+ str(offset_x) +" -offset_y "+ str(offset_y) +" -i desktop -frames:v 1 -draw_mouse 1 " + filename, shell=True)
        if res:
            temp = ["failed!","截图失败"]
        else:
            temp = ["success!",filename]
        self.signal.emit(temp)
        return temp[1]

    def begingif(self,offset_x = 0, offset_y = 0, width = 1920, height = 1080, fps = 15, draw_mouse = 0):
        filename = config['GIF']['filepath'] + str(int(time.time() * 1000))+".mp4"
        self.process = subprocess.Popen("ffmpeg -f gdigrab -s "+ str(width) +"x"+ str(height) +" -offset_x "+ str(offset_x) +" -offset_y "+ str(offset_y) +" -i desktop -draw_mouse 1 -framerate 15 " + filename,shell=True, stdin=subprocess.PIPE)
        self.filename = filename
        self.width = width

    def endgif(self):
        self.process.communicate(str.encode("q"))
        self.process.wait()
        res1 = subprocess.call("ffmpeg -i "+ self.filename +" -vf fps=12,scale="+str(self.width)+":-1:flags=lanczos,palettegen -y "+ self.filename.replace("mp4","png"), shell=True)
        res2 = subprocess.call("ffmpeg -i "+ self.filename +" -i "+ self.filename.replace("mp4","png") +" -lavfi \"fps=12,scale="+str(self.width)+":-1:flags=lanczos[x];[x][1:v]paletteuse\" -y "+ self.filename.replace("mp4","gif"), shell=True)
        res3 = subprocess.call("del "+ self.filename.replace("mp4","png"), shell=True)
        res4 = subprocess.call("del "+ self.filename, shell=True)
        if res1 or res2 or res3 or res4:
            temp = ["failed!","录制GIF失败"]
        else:
            temp = ["success!",self.filename.replace("mp4","gif")]
        self.signal.emit(temp)
        return temp[1]






# 测试截屏和录屏
# gif1 = GIF()
# gif1.screencut()
# gif1.begingif()
# time.sleep(10)
# gif1.screencut(100,100,600,600)
# gif1.endgif()
# time.sleep(10)
# gif1.begingif(offset_x = 100, offset_y = 100, width = 600, height = 600)
# time.sleep(10)
# gif1.endgif()