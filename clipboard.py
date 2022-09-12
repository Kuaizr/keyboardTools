import io,time,sys
from PIL import Image
import subprocess
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QGuiApplication
def get_clipboard():
    return subprocess.check_output(['xsel','-o','-b']).decode("utf-8")

def set_clipboard(str):
    res = subprocess.run("echo "+str+" | xsel -i -b",shell=True)
    return res.returncode

def image2byte(image):
    '''
    图片转byte
    image: 必须是PIL格式
    image_bytes: 二进制
    '''
    # 创建一个字节流管道
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="png")
    # # 从字节流管道中获取二进制
    image_bytes = img_bytes.getvalue()
    return image_bytes

def getClipBoardImg():
    app = QGuiApplication(sys.argv)
    time.sleep(1)
    cb = QApplication.clipboard()
    if cb.mimeData().hasImage():
        qt_img = cb.image()
        pil_img = Image.fromqimage(qt_img)  # 转换为PIL图像
        return image2byte(pil_img)
    else:
        return "no img need to upload"
print(getClipBoardImg())
#print(get_clipboard())
#cstr='剪贴板'
#写入
#print(set_clipboard(cstr))
#读取并输出
#print(get_clipboard())
