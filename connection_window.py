from PyQt5 import QtWidgets


class ConnectionWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ip = QtWidgets.QLineEdit('192.168.1.3')
        self.port = QtWidgets.QLineEdit('12345')
        self.nickname = QtWidgets.QLineEdit()

        self._buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)

        text_fields_layout = self.get_text_fields_layout()

        layout = QtWidgets.QVBoxLayout()
        layout.setSpacing(5)
        layout.addLayout(text_fields_layout)
        layout.addWidget(self._buttons)

        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)

        self.setWindowTitle('Start chat')
        self.setLayout(layout)

    def get_text_fields_layout(self):
        layout = QtWidgets.QGridLayout()
        layout.setSpacing(5)
        layout.addWidget(QtWidgets.QLabel('Server IP: '), 0, 0)
        layout.addWidget(self.ip, 0, 1)
        layout.addWidget(QtWidgets.QLabel('Port: '), 1, 0)
        layout.addWidget(self.port, 1, 1)
        layout.addWidget(QtWidgets.QLabel('Nickname'), 2, 0)
        layout.addWidget(self.nickname, 2, 1)
        return layout

