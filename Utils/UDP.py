import socket
from PyQt5.QtCore import *
from Utils.Config import config

class UDP(QThread):
    signal = pyqtSignal(list)
    def __init__(self) -> None:
        super(UDP,self).__init__()
        self.serverPort=config['UDP']['port']
        self.serverSocket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.ipv4 = socket.gethostbyname(socket.gethostname())
        self.serverSocket.bind((str(self.ipv4),self.serverPort))
        self.clientAddress = (config['UDP']['Client']['ipv4'], config['UDP']['Client']['port'])
        
    def sendInfo(self,message):
        try:
            self.serverSocket.sendto(message, self.clientAddress)
        except:
            self.signal.emit(["failed!","客户端地址格式有问题，请修改"])

    def changeClient(self,ipv4,port):
        self.clientAddress = (ipv4, int(port))