#!/usr/bin/env python3

import sys
from PyQt5 import QtWidgets
from PyQt5 import QtNetwork
from PyQt5.QtNetwork import QHostAddress


class ConnectionWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._ip = QtWidgets.QLineEdit('127.0.0.1')
        self._port = QtWidgets.QLineEdit('12345')
        self._buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        layout2 = QtWidgets.QGridLayout()
        layout2.setSpacing(5)
        layout2.addWidget(QtWidgets.QLabel('Server IP: '), 0, 0)
        layout2.addWidget(self._ip, 0, 1)
        layout2.addWidget(QtWidgets.QLabel('Port: '), 1, 0)
        layout2.addWidget(self._port, 1, 1)

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(5)
        layout.addLayout(layout2)
        layout.addWidget(self._buttons)

        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)

        self.setLayout(layout)


class ChatWindow(QtWidgets.QMainWindow):
    def _connect(self):
        try:
            self._ip = self._conn_dialog._ip_text()
            self._port = int(self._conn_dialog._port.text())
        except Exception as e:
            self.statusBar.showMessage('Connection error: {}'.format(e))
            return
        self.statusBar.showMessage("Connecting to {}, {}".format(self._ip, self._port))
        self._sock.connectToHost(self._ip, self._port)

    def _send(self):
        _text = self._input.text()
        if not _text:
            return

        self._input.setText('')
        self._sock._write(_text.encode(errors='replace'))
        self._messages.append("Me: {}".format(_text))

    def _connected(self):
        self.statusBar().showMessage('Connected!')
        self._send_button.setDisabled(False)

    def _disconnected(self):
        self.statusBar().showMessage('Disconnected!')
        self._send_button.setDisabled(True)

    def _read(self):
        while self._sock.bytesAvailable():
            message = self._sock.readAll().data().decode(errors='replace')
            self._messages.append(message)

    def get_params(self):
        self.__conn_dialog.show()

    def _connect(self):
        print('Connect!')

    def _turn_on_sendButton(self):
        self._send_button.setDisabled(False)

    def __init__(self, parent=None):
        super().__init__(parent)

        self._sock = QtNetwork.QTcpSocket()
        self._sock.connected.connect(self._connected)
        self._sock.disconnected.connect(self._disconnected)
        self._sock.readyRead.connect(self._read)

        self.statusBar().showMessage('Waiting for params...')

        self._conn_dialog = ConnectionWindow(parent)
        self._conn_dialog.setModal(True)
        self._conn_dialog.accepted.connect(self._connect)
        self._conn_dialog.rejected.connect(self.close)
        self._conn_dialog.show()

        self._sock.bind(QHostAddress.LocalHost, 12345)

        self._input = QtWidgets.QLineEdit()
        self._send_button = QtWidgets.QPushButton('&Send')
        self._send_button.setDisabled(True)
        self._input.returnPressed.connect(self._send_button.click)
        self._send_button.clicked.connect(self._send)

        self._sock.connected.connect(self._turn_on_sendButton)

        self._messages = QtWidgets.QTextEdit()
        self._messages.setReadOnly(True)

        _layout = QtWidgets.QGridLayout()
        _layout.setSpacing(5)
        _layout.addWidget(self._messages, 0, 0, 1, 2)
        _layout.addWidget(self._input, 1, 0)
        _layout.addWidget(self._send_button, 1, 1)

        _window = QtWidgets.QWidget()
        _window.setLayout(_layout)
        self.setCentralWidget(_window)

        self.resize(400, 300)

    # self.setWindowTile('Chat')


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = ChatWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
