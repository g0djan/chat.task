from PyQt5 import QtNetwork
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtNetwork import QHostAddress


class Client(QObject):
    def __init__(self, callWindow):
        super().__init__()
        self.callWindow = callWindow
        self.udpSocket = QtNetwork.QUdpSocket(self)
        self.udpSocket.bind(QHostAddress.LocalHost, 45454)
        self.udpSocket.readyRead.connect(callWindow.emit)

    def readPendingDatagrams(self):
        data = ''
        while self.udpSocket.hasPendingDatagrams():
            datagram, host, port = self.udpSocket.readDatagram(self.udpSocket.pendingDatagramSize())
            data += str(datagram, encoding='ascii')
        return data

    def send(self, msg):
        self.udpSocket.writeDatagram(msg, QHostAddress.LocalHost, 45454)


class Message:
    def __init__(self, message, owner):
        self.message = message
        self.owner = owner


class Session:
    def __init__(self):
        self.messages = []


class Window(QtWidgets.QDialog):
    needAddMessage = pyqtSignal()

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.client = Client(self.needAddMessage)
        self.statusLabel = QtWidgets.QLabel("Listening for broadcasted messages")
        quitButton = QtWidgets.QPushButton("&Quit")
        quitButton.clicked.connect(self.close)
        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(quitButton)
        buttonLayout.addStretch(1)
        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addWidget(self.statusLabel)
        mainLayout.addLayout(buttonLayout)
        self.setLayout(mainLayout)
        self.setWindowTitle("Broadcast Receiver")
        self.needAddMessage.connect(self.printMsg)

    def printMsg(self):
        self.statusLabel.setText(self.client.readPendingDatagrams())


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    #  receiver.send(b'work')
    window.client.send(b'blyaOMGOOOOOOOOOOOOOOff')
    window.show()
    sys.exit(app.exec_())
