import time
from Utils.clipboard import set_clipboard, get_clipboard, getImgLableToMarkdown, getImgLableBybase64
import keyboard
from Utils.youdao import youdao
from Utils.GIF import GIF
from Utils.Translation import Translation
from Utils.Config import config

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
        handelClipboard(result)
    else:
        print("编码不支持")

def handelClipboard(info):
    if info[-3:] == "gif" or info[-3:] == "png":
        if config["imgType"] == "path":
            set_clipboard(info)
        elif config["imgType"] == "markdown":
            info = getImgLableToMarkdown(info)
            print(info)
            set_clipboard(info)
        elif config["imgType"] == "base64":
            info = getImgLableBybase64(info)
            print(info)
            set_clipboard(info)
    else:
        print(info)
        set_clipboard(info)

def screencut(gif):
    res = gif.screencut()
    handelClipboard(res)

def gifbegin(gif,hasGif):
    if hasGif['value'] == False:
        gif.begingif()
        hasGif['value'] = True

def gifend(gif,hasGif):
    if hasGif['value']:
        hasGif['value'] = False
        res = gif.endgif()
        handelClipboard(res)

def escfun(hasGif):
    if hasGif['value']:
        hasGif['value'] = False
        gif.endgif()
        print("录制中断")

def record(translation,hasRecord):
    if hasRecord['value'] == False:
        hasRecord['value'] = True
        translation.start()
    else:
        hasRecord['value'] = False
        translation.stop()
        translation.terminate()
    
if __name__ == '__main__':

    mark ={'value': 0}
    keyboard.add_hotkey('ctrl+c', timimg,args=(mark,),suppress = False)

    hasGif = {'value': False}
    gif = GIF()
    keyboard.add_hotkey('ctrl+shift+[', gifbegin, args=(gif,hasGif) ,suppress = False)
    keyboard.add_hotkey('ctrl+shift+]', gifend, args=(gif,hasGif) ,suppress = False)
    keyboard.add_hotkey('ctrl+shift+a', screencut, args=(gif,),suppress = False)
    keyboard.add_hotkey('esc', escfun, args=(hasGif,) ,suppress = False)

    if config["Translation"]["enable"]:
        hasRecord = {'value': False}
        translation = Translation()
        keyboard.add_hotkey('ctrl+shift+t', record, args=(translation,hasRecord) ,suppress = False)
    
    keyboard.wait()
