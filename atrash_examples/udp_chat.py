from PyQt5 import QtWidgets
from PyQt5.QtNetwork import QHostInfo, QUdpSocket, QHostAddress

udp_port = 45454


class GreetingWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._nick = QtWidgets.QLineEdit()
        self._buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        layout2 = QtWidgets.QGridLayout()
        layout2.setSpacing(5)
        layout2.addWidget(QtWidgets.QLabel('Nickname: '), 0, 0)
        layout2.addWidget(self._nick, 0, 1)

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(5)
        layout.addLayout(layout2)
        layout.addWidget(self._buttons)
        self.enabling_button("")
        self._nick.textEdited.connect(self.enabling_button)
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)
        self.setLayout(layout)

    def enabling_button(self, text):
        self._buttons.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(bool(text))


class ChatBox(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ChatBox, self).__init__(parent)
        self.hostInfo = QHostInfo(1)
        self.udpSocket = QUdpSocket(self)
        self.udpSocket.bind(udp_port)
        self.udpSocket.readyRead.connect(self._readPendingDatagrams)

        self.sendButton = QtWidgets.QPushButton("&Send")
        self.sendButton.clicked.connect(self._send)
        self.textBox = QtWidgets.QTextEdit()
        self.textBox.setReadOnly(True)

        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addWidget(self.sendButton)
        textLayout = QtWidgets.QHBoxLayout()
        textLayout.addWidget(self.textBox)
        self.input = QtWidgets.QLineEdit()
        lineEditBox = QtWidgets.QHBoxLayout()
        lineEditBox.addWidget(self.input)

        mainLayout = QtWidgets.QVBoxLayout()
        mainLayout.addLayout(textLayout)
        mainLayout.addLayout(lineEditBox)
        mainLayout.addLayout(buttonLayout)
        self.resize(1024, 1024)

        self.setLayout(mainLayout)
        self.setWindowTitle('pizhe than telegram')

        self.greeting = GreetingWindow()
        self.greeting.accepted.connect(self.change_nick)
        self.greeting.finished.connect(self.show)

    def _send(self):
        msg = bytearray(self._nick + ': ' + self.input.text(), encoding='ascii')
        self.input.clear()
        self.udpSocket.writeDatagram(msg, QHostAddress.Broadcast, udp_port)

    def _readPendingDatagrams(self):
        data = ''
        while self.udpSocket.hasPendingDatagrams():
            datagram, host, port = self.udpSocket.readDatagram(self.udpSocket.pendingDatagramSize())
            data += str(datagram, encoding='ascii')
        self.textBox.append(data)

    def change_nick(self):
        self._nick = self.greeting._nick.text()


class Message:
    def __init__(self, message, owner):
        self.message = message
        self.owner = owner


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    chatBox = ChatBox()
    chatBox.greeting.show()
    sys.exit(app.exec_())
