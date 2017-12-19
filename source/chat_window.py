from PyQt5 import QtWidgets
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QFileDialog

from source.connection_window import ConnectionWindow
from source.file_worker import FileWorker, File
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
        self.statusBar().showMessage('Disconnected!')
        self.resize(800, 600)

    def _add_controls(self):
        self._input = QtWidgets.QLineEdit()
        self._send_file_button = QtWidgets.QPushButton('&Send file')
        self._send_button = QtWidgets.QPushButton('&Send')
        self._messages = QtWidgets.QTextEdit()
        self._online = QtWidgets.QTextEdit()
        self._messages.setReadOnly(True)
        self._online.setReadOnly(True)
        self._online.setFixedWidth(200)

    def _set_event_reactions(self):
        self._input.returnPressed.connect(self._send_button.click)
        self._send_button.clicked.connect(self._send)
        self._send_file_button.clicked.connect(self._send_file)

    def _get_layout(self):
        layout = QtWidgets.QGridLayout()
        layout.setSpacing(5)
        layout.addWidget(self._online, 0, 2, 1, 1)
        layout.addWidget(self._messages, 0, 0, 1, 2)
        layout.addWidget(self._input, 1, 0)
        layout.addWidget(self._send_button, 1, 1)
        layout.addWidget(self._send_file_button, 1, 2)
        layout.setColumnStretch(2, 1)
        return layout

    def _update_message_box(self):
        if self.server.last_message.mode != Mode.Normal:
            return
        message = self.server.last_message.content
        self._messages.append(message)

    def _connect(self):
        ip = self._conn_dialog.ip.text()
        port = int(self._conn_dialog.port.text())
        nickname = self._conn_dialog.nickname.text()
        self.server = Server(nickname, port, self)
        self.server.has_new_message.connect(self._update_message_box)
        self.server.has_new_message.connect(self.server.resend)
        self.server.change_connections_cnt.connect(self._set_connection_status)
        self.server.peer_manager.set_connection(ip, port)

    def _send(self):
        ip = self.server.client_info.ip
        recipient, text = self._get_recipient()
        content = self.server.client_info.name + ': ' + text
        message = Message(ip, content, Mode.Normal, recipient)
        self.server.add_new_message(message)
        self._input.setText('')

    def _get_recipient(self):
        parts = self._input.text().split(':', 1)
        if len(parts) == 1:
            return 'all', self._input.text()
        if parts[0][:3] == 'to ':
            return parts[0][3:], parts[1]
        return 'all', self._input.text()

    def _set_connection_status(self):
        if len(self.server.connections.keys()) == 0:
            self.statusBar().showMessage('Disconnected!')
        else:
            self.statusBar().showMessage('Connected!')

    def _send_file(self):
        filename = self._select_file()
        if not filename:
            return
        file = File(filename)
        ip = self.server.client_info.ip
        recipient, text = self._get_recipient()
        message = Message(ip, file, Mode.File, recipient)
        self.server.add_new_message(message)
        self._input.setText('')

    def get_folder(self):
        return self._select_folder()

    def _select_file(self):
        selected_file = QFileDialog.getOpenFileNames(self, 'Choose file', QDir.currentPath(), 'All files (*.*)')
        if len(selected_file[0]) == 0:
            return ''
        return selected_file[0][0]

    def _select_folder(self):
        return QFileDialog.getExistingDirectory(self, 'Choose directory', QDir.currentPath())

    def say_he_is_online(self, name):
        self._messages.append('meet the ' + name + ', he is online')

    def say_he_is_offline(self, name):
        self._messages.append('Bye! Bye! ' + name + ' is offline')

    def refresh_online_and_connections(self, online, connections):
        info = 'online:\n'
        for ip in online:
            info += ' ' + online[ip].name + '\n'
        info += '\nconnections:\n'
        for ip in connections:
            info += ' ' + ip + '\n'
        self._online.setText(info)
