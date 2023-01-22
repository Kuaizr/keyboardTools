import socket
from PyQt5.QtCore import *
from Utils.Config import config

def get_host_ip():
     """
     查询本机ip地址
     :return: ip
     """
     try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
     finally:
        s.close()
     return ip

class UDP(QThread):
    signal = pyqtSignal(list)
    def __init__(self) -> None:
        super().__init__()
        self.serverPort=config['UDP']['port']
        self.serverSocket=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.ipv4 = get_host_ip()
        self.serverSocket.bind((str(self.ipv4),self.serverPort))
        self.clientAddress = (config['UDP']['Client']['ipv4'], config['UDP']['Client']['port'])
        
    def sendInfo(self,message):
        try:
            self.serverSocket.sendto(message, self.clientAddress)
        except:
            self.signal.emit(["failed!","客户端地址格式有问题，请修改"])

    def changeClient(self,ipv4,port):
        self.clientAddress = (ipv4, int(port))