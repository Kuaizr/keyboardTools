import time
from ImgBed import ImageBed
from clipboard import set_clipboard, get_clipboard
import keyboard
from youdao import youdao
from GIF import GIF



def uploadimg(imgbed):
    result = imgbed.pushimg()
    print(result)
    set_clipboard(result)

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
    if word:
        result = youdao(word)
        print(result)
    else:
        print("编码不支持")


def screencut(gif):
    res = gif.screencut()
    print(res)
    set_clipboard(res)

    

def gifbegin(gif,hasGif):
    if hasGif['value'] == False:
        gif.begingif()
        hasGif['value'] = True

def gifend(gif,hasGif):
    if hasGif['value']:
        hasGif['value'] = False
        res = gif.endgif()
        print(res)
        set_clipboard(res)

def escfun(hasGif):
    if hasGif['value']:
        hasGif['value'] = False
        gif.endgif()
        print("录制中断")
    


if __name__ == '__main__':
    mark ={'value': 0}
    hasGif = {'value': False}
    # 初始化ImgBed
    imgbed = ImageBed()
    # 初始化GIF
    gif = GIF()

    keyboard.add_hotkey('ctrl+alt', uploadimg, args=(imgbed,) ,suppress = False)
    keyboard.add_hotkey('ctrl+c', timimg,args=(mark,),suppress = False)
    keyboard.add_hotkey('ctrl+shift+[', gifbegin, args=(gif,hasGif) ,suppress = False)
    keyboard.add_hotkey('ctrl+shift+]', gifend, args=(gif,hasGif) ,suppress = False)
    keyboard.add_hotkey('ctrl+shift+a', screencut, args=(gif,),suppress = False)
    keyboard.add_hotkey('esc', escfun, args=(hasGif,) ,suppress = False)
    keyboard.wait()
