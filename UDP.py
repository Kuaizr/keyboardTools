from socket import *
from PyQt5.QtCore import *
import time

class UDP(QThread):
    def __init__(self) -> None:
        super(UDP).__init__()
        self.serverPort=12000
        self.serverSocket=socket(AF_INET,SOCK_DGRAM)
        self.serverSocket.bind(("192.168.58.157",self.serverPort))
        self.clientAddress = ("192.168.3.9", 12345)
            
    def sendInfo(self,message):
        self.serverSocket.sendto(message, self.clientAddress)
