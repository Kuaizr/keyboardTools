### 环境

python

### 主要用到的几个库

pywin32

keyboard

pyqt5

socket

request

ffmpeg(系统环境内部的)

### 用处

我用halo搭了一个个人博客，博客可以上传文件和图片，所以我就顺便做了一个图床，这个程序可以让本地剪切板的图片经过热键上传到图床，并返回markdown格式，后面为了方便，本来我是用微信截图，然后存到剪切板的，后来发现有时候图片不能很好的展示我的操作，我希望可以使用gif来录制，所以我使用ffmpeg+pyqt5的方式自己做了一个框选截图和框选录制gif的工具，我还利用剪切板和有道翻译做了一个全局剪切板翻译的功能。

### 11月10日更新

增加了UDP连接的支持，增加了系统托盘图标，增加了写markdown时可以直接嵌入图片的选项

### 需要注意的事情

程序的入口有两个分别是GUI.py和terminal.py，一个是带图形化界面的，一个不带，输出都在命令行里面，如果想使用terminal.py且完全摆脱pyqt5的依赖，可以把GIF.py中的有关QThread和pyqtSingal的东西去掉。

### 1月21号更新

利用whisper添加了实时语音字幕得功能，

主要用到的库

whisper

opencc-python-reimplemented

pyaudio

torch

numpy

等等

### 1月22号更新

重构了整个代码文件，添加了UDP的客户端修改操作界面，添加了Config.py对整个系统做启动配置
