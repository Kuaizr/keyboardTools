### 环境

python

### 主要用到的几个库

pip install keyboard pyqt5

ffmpeg

### 用处

我用python写了个截图工具，该工具还可以录制gif，还利用剪切板和有道翻译做了一个全局剪切板翻译的功能。

### 需要注意的事情

程序的入口有两个分别是GUI.py和terminal.py，一个是带图形化界面的，一个不带，输出都在命令行里面，如果想使用terminal.py且完全摆脱pyqt5的依赖，可以把GIF.py中的有关QThread和pyqtSingal的东西去掉。

### linux版本

和windows版本区别不大，主要是ffmpeg使用时windows用的是gdigrab，linux用的是x11grab，然后取消了gif录制的红框（这是因为我使用的dwm和picom在窗口的渲染时宽度的gap有自己的想法，我又懒得自己设置）

linux的剪切板是用xsel实现的
