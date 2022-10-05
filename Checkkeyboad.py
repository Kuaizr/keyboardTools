import time
from ImgBed import ImageBed
from clipboard import set_clipboard, get_clipboard
import keyboard
from youdao import youdao
# from MessageBox import showInfo



def uploadimg(imgbed):
    result = imgbed.pushimg()
    print(result)
    set_clipboard(result)
    # showInfo(result)

def timimg(mark):
    if mark['value'] == 0:
        mark['value'] = time.time() * 1000
    else:
        marktime = int(time.time() * 1000 - mark['value'])
        if marktime <= 500:
            mark['value'] = 0
            fanyi()
        else:
            mark['value'] = 0
            timimg(mark)

def fanyi():
    word = get_clipboard()
    result = youdao(word)
    print(result)
    # showInfo(result)


if __name__ == '__main__':
    mark ={'value': 0}
    # 初始化ImgBed
    imgbed = ImageBed()
    keyboard.add_hotkey('ctrl+alt', uploadimg, args=(imgbed,) ,suppress = False)
    keyboard.add_hotkey('ctrl+c', timimg, args=(mark,),suppress = False)
    keyboard.wait()
