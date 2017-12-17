from PyQt5 import QtWidgets

from source.connection_window import ConnectionWindow
from source.message import Message, Mode
from source.server import Server


class ChatWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._conn_dialog = ConnectionWindow(parent)
        self._conn_dialog.setModal(True)
        self._conn_dialog.accepted.connect(self._connect)
        self._conn_dialog.rejected.connect(self.close)
        self._conn_dialog.show()

        self._add_controls()
        self._set_event_reactions()

        _window = QtWidgets.QWidget()
        _window.setLayout(self._get_layout())
        self.setCentralWidget(_window)

        self.resize(400, 300)

    def _add_controls(self):
        self._input = QtWidgets.QLineEdit()
        self._send_button = QtWidgets.QPushButton('&Send')
        self._messages = QtWidgets.QTextEdit()
        self._messages.setReadOnly(True)

    def _set_event_reactions(self):
        self._input.returnPressed.connect(self._send_button.click)
        self._send_button.clicked.connect(self._send)


    def _get_layout(self):
        layout = QtWidgets.QGridLayout()
        layout.setSpacing(5)
        layout.addWidget(self._messages, 0, 0, 1, 2)
        layout.addWidget(self._input, 1, 0)
        layout.addWidget(self._send_button, 1, 1)
        return layout

    def _update_message_box(self):
        message = self.server.last_message.content
        self._messages.append(message)

    def _connect(self):
        ip = self._conn_dialog.ip.text()
        port = int(self._conn_dialog.port.text())
        nickname = self._conn_dialog.nickname.text()
        self.server = Server(nickname, port)
        self.server.has_new_message.connect(self._update_message_box)
        self.server.has_new_message.connect(self.server.resend)
        self.server.change_connections_cnt.connect(self._set_connection_status)
        self.server.peer_manager.set_connection(ip, port)

    def _send(self):
        ip = self.server.client_info.ip
        content = self.server.client_info.name + ':' + self._input.text()
        message = Message(ip, content, Mode.Normal)
        self.server.add_new_message(message)
        self._input.setText('')

    def _set_connection_status(self):
        if len(self.server.connections.keys()) == 0:
            self.statusBar().showMessage('Disconnected!')
        else:
            self.statusBar().showMessage('Connected!')
