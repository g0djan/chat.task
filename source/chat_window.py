import os
from PyQt5 import QtWidgets
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QFileDialog

from source.connection_window import ConnectionWindow
from source.file_worker import File
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
        self._messages = QtWidgets.QTextEdit()
        self._messages.setReadOnly(True)
        self._input = QtWidgets.QTextEdit()
        self._input.setFixedHeight(23)
        self._send_button = QtWidgets.QPushButton('&Send')
        self._send_button.setFixedHeight(25)
        self._send_button.setEnabled(False)
        self._input.textChanged.connect(self._enable_send_button)
        self._change_nick_label = QtWidgets.QLabel('Change nickname')
        self._change_nick_label.setFixedWidth(120)
        self._change_nick_button = QtWidgets.QPushButton('&Change')
        self._change_nick_button.setEnabled(False)
        self._change_nick = QtWidgets.QLineEdit()
        self._change_nick.setFixedWidth(200)
        self._change_nick.textEdited.connect(self._enable_change_button)
        self._change_nick.returnPressed.connect(self._change_nick_button.click)
        self._change_nick_button.clicked.connect(self._change_nickname)
        self._online = QtWidgets.QTextEdit()
        self._online.setReadOnly(True)
        self._online.setFixedWidth(200)
        self._send_file_button = QtWidgets.QPushButton('&Send file')
        self._send_file_button.setFixedHeight(25)

    def _enable_send_button(self):
        self._send_button.setEnabled(bool(self._input.toPlainText()))

    def _enable_change_button(self, text):
        self._change_nick_button.setEnabled(bool(text))

    def _set_event_reactions(self):
        # self._input.returnPressed.connect(self._send_button.click)
        self._send_button.clicked.connect(self._send)
        self._send_file_button.clicked.connect(self._send_file)

    def _change_nickname(self):
        self.server.client_info.change_name(self._change_nick.text())
        self.server.update_client_info()
        self._change_nick.setText('')

    def _get_layout(self):
        layout = QtWidgets.QGridLayout()
        layout.setSpacing(5)
        layout.addWidget(self._messages, 0, 0, 3, 2)
        layout.addWidget(self._input, 3, 0)
        layout.addWidget(self._send_button, 3, 1)
        layout.addWidget(self._change_nick_label, 0, 2)
        layout.addWidget(self._change_nick_button, 0, 3)
        layout.addWidget(self._change_nick, 1, 2, 1, 2)
        layout.addWidget(self._online, 2, 2, 1, 2)
        layout.addWidget(self._send_file_button, 3, 2, 1, 2)
        layout.setColumnStretch(2, 1)
        return layout

    def _update_message_box(self):
        if self.server.last_message.mode != Mode.Normal:
            return
        message = self.server.last_message.content
        with open(os.path.join('logs', 'log'), 'a') as f:
            f.write(message + '\n')
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
        parts = self._input.toPlainText().split(':', 1)
        if len(parts) == 1:
            return 'all', self._input.toPlainText()
        if parts[0][:3] == 'to ':
            return parts[0][3:], parts[1]
        return 'all', self._input.toPlainText()

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
        text = 'meet the ' + name + ', he is online'
        with open(os.path.join('logs', 'log'), 'a') as f:
            f.write(text + '\n')
        self._messages.append(text + '\n')

    def say_he_is_offline(self, name):
        text = 'Bye! Bye! ' + name + ' is offline'
        with open(os.path.join('logs', 'log'), 'a') as f:
            f.write(text + '\n')
        self._messages.append(text)

    def refresh_online_and_connections(self, online, connections):
        info = 'online:\n'
        for ip in online:
            info += ' ' + online[ip].name + '\n'
        info += '\nconnections:\n'
        for ip in connections:
            info += ' ' + ip + '\n'
        self._online.setText(info)
