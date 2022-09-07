import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from qt_material import apply_stylesheet
 
class MessageBox(QWidget):#继承QMainWindow类,继承就是把QMainWindow类的所有方法和变量继承过来。
    def __init__(self):#创建子类__init__方法
        super().__init__()
        self.desktop = QApplication.desktop()
#        self.animationbegin = QPropertyAnimation(self, b'geometry')
#        self.animationbegin.setDuration(2000)
#        self.animationbegin.setStartValue(QRect(-300,0,300,120))
#        self.animationbegin.setEndValue(QRect(0,0,300,120))
#        self.animationbegin.start()
        self.animationend = None
        self.ui()
    def ui(self):
        self.resize(300,120)#窗口大小
        self.setFixedSize(self.width(),self.height())#设置窗口大小不可变
        self.setWindowFlags(Qt.FramelessWindowHint)
    
    def closeEvent(self, event):
        if self.animationend is None:
            self.animationend = QPropertyAnimation(self, b'geometry')
            self.animationend.setDuration(600)
            self.animationend.setStartValue(QRect(0,27,300,120))
            self.animationend.setEndValue(QRect(-300,27,300,120))
            self.animationend.finished.connect(self.close)
            self.animationend.start()
            event.ignore()
#主程序
if __name__ == '__main__':
    application=QApplication(sys.argv)#窗口通讯
    apply_stylesheet(application, theme='dark_teal.xml')
    root=MessageBox()#创建对象
    root.resize(230,100)
    root.show()#展示窗口
    QTimer.singleShot(3000, root.close)
    sys.exit(application.exec_())
