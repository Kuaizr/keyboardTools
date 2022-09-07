
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
 
class Main(QMainWindow):#继承QMainWindow类,继承就是把QMainWindow类的所有方法和变量继承过来。
    def __init__(self):#创建子类__init__方法
        super().__init__()
        self.ui()
    def ui(self):
        #设置窗口
        self.setWindowTitle('Test')#窗口标题
        # self.resize(700,450)#窗口大小
        self.setFixedSize(self.width(),self.height())#设置窗口大小不可变
#主程序
if __name__ == '__main__':
    application=QApplication(sys.argv)#窗口通讯
    root=Main()#创建对象
    root.show()#展示窗口
    sys.exit(application.exec_())#消息循环
