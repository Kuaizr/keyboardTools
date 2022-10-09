import ffmpeg
import time
import subprocess
from PyQt5.QtCore import *
 
# 屏幕录制画面大小
class GIF(QThread):
    signal = pyqtSignal(list)
    def __init__(self):
        super().__init__()

        #ffmpeg 录制视频 -> 调色板 -> gif
        
    def begingif(self,offset_x = 0, offset_y = 0, width = 1920, height = 1080, fps = 30, draw_mouse = 0):
        filename = str(int(time.time() * 1000))+".mp4"
        self.process = (
                    ffmpeg
                    .input(filename='desktop', format='gdigrab', framerate=fps, offset_x=offset_x, offset_y=offset_y,draw_mouse=draw_mouse, s=f'{width}x{height}')
                    .output(filename)
                    .overwrite_output()
                    .run_async(pipe_stdin=True,pipe_stdout=False)
        )
        self.filename = filename
        self.width = width

    def endgif(self):
        print("-------------------------------------------------------------------------------------------------------------------------")
        self.process.communicate(str.encode("q"))
        self.process.terminate()
        subprocess.call("ffmpeg -i "+ self.filename +" -vf fps=20,scale="+str(self.width)+":-1:flags=lanczos,palettegen -y "+ self.filename.replace("mp4","png"), shell=True)
        subprocess.call("ffmpeg -i "+ self.filename +" -i "+ self.filename.replace("mp4","png") +" -lavfi \"fps=15,scale="+str(self.width)+":-1:flags=lanczos[x];[x][1:v]paletteuse\" -y "+ self.filename.replace("mp4","gif"), shell=True)
        subprocess.call("del "+ self.filename.replace("mp4","png"), shell=True)
        subprocess.call("del "+ self.filename, shell=True)

# gif1 = GIF()
# gif1.begingif()
# time.sleep(10)
# gif1.endgif()
# time.sleep(10)

# gif1.begingif(offset_x = 100, offset_y = 100, width = 600, height = 600)
# time.sleep(10)
# gif1.endgif()