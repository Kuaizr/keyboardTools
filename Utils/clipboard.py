from PIL import Image, ImageGrab
import os
import base64
import io
import win32con,time
from win32clipboard import GetClipboardData, OpenClipboard, CloseClipboard, EmptyClipboard,SetClipboardData

# 读取剪贴板的文本数据
def get_clipboard():
    OpenClipboard()
    d = GetClipboardData(win32con.CF_TEXT)
    try:
        CloseClipboard()
    except:
        pass
    try:
        result = d.decode("GBK")
        return result
    except:
        return None

#写入剪贴板数据
def set_clipboard(astr):
    OpenClipboard()
    EmptyClipboard()
    time.sleep(1)
    SetClipboardData(win32con.CF_UNICODETEXT, astr)
    CloseClipboard()


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
    im = ImageGrab.grabclipboard()
    if isinstance(im, Image.Image):
        return image2byte(im)
    else:
        path = get_clipboard().strip()
        if path.endswith("png"):
            # 判断文件是否存在
            if os.path.exists(path):
                f = open(path,'rb')
                imgdate = f.read()
                f.close()
                return [imgdate,'png']
        elif path.endswith("gif"):
            if os.path.exists(path):
                f = open(path,'rb')
                imgdate = f.read()
                f.close()
                return [imgdate,'gif']
        else:
            pass
    
def getImgLableBybase64(path):
    pic = ""
    if os.path.exists(path):
        f = open(path,'rb')
        imgdate = f.read()
        f.close()
        s = base64.b64encode(imgdate)
        pic=s.decode('ascii')
    return "<img src='data:image/png;base64,"+ pic +"'/>"

def getImgLableToMarkdown(path):
    return "![]("+ path +")"

