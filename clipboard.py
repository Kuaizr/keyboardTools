import os
import base64
import subprocess
def get_clipboard():
    return subprocess.check_output(['xsel','-o','-b']).decode("utf-8")

def set_clipboard(str):
    res = subprocess.run("echo "+str+" | xsel -i -b",shell=True)
    return res.returncode

def getClipBoardImg():
    path = get_clipboard().strip()
    if path.endswith("png"):
        # 判断文件是否存在
        if os.path.exists(path):
            f = open(path,'rb')
            imgdate = f.read()
            f.close()
            return [imgdate,'png']
        return ["no img need to upload","png"]
    elif path.endswith("gif"):
        if os.path.exists(path):
            f = open(path,'rb')
            imgdate = f.read()
            f.close()
            return [imgdate,'gif']
        return ["no img need to upload","png"]
    else:
        return ["no img need to upload","png"]

def getImgLableBybase64(path):
    pic = ""
    if os.path.exists(path):
        f = open(path,'rb')
        imgdate = f.read()
        f.close()
        s = base64.b64encode(imgdate)
        pic=s.decode('ascii')
    return "<img src='data:image/png;base64,"+ pic +"'/>"

