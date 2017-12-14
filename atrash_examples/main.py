from PyQt5 import QtNetwork
from PyQt5.QtCore import QObject
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtNetwork import QHostAddress

HOST = '127.0.0.1'
PORT = 12345


class Client(QObject):
    trigger = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=None)
        self.udpSocket = QtNetwork.QUdpSocket(self)
        self.udpSocket.bind(QHostAddress.LocalHost, 1234)
        self.udpSocket.readyRead.connect(self.printer)#self.udpSocket.readDatagram(1024))
        self.udpSocket.da

    def connect_and_emit(self):
        self.trigger.connect(self.printer)
        self.trigger.emit()

    def send(self):
        self.udpSocket.writeDatagram(b'pezdos')

    def printer(self):
        print('aue')



def main():
    client = Client()
    client.send()
    #client.connect_and_emit()


if __name__ == '__main__':
    main()
