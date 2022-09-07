
from ImgBed import ImageBed
from clipboard import set_clipboard, get_clipboard
import keyboard
from youdao import youdao


def uploadimg(imgbed):
    result = imgbed.pushimg()
    print(result)
    set_clipboard(result)

def fanyi():
    word = get_clipboard()
    print(youdao(word))


if __name__ == '__main__':
    # 初始化ImgBed
    imgbed = ImageBed()
    # keyboard.add_hotkey('f1', test_a)
    keyboard.add_hotkey('ctrl+alt', uploadimg, args=(imgbed,))
    keyboard.add_hotkey('ctrl+shift+c', fanyi)
    keyboard.wait()
