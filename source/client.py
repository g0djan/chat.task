import threading
from pickle import PickleError

from PyQt5.QtCore import QObject, QThread, pyqtSignal, QIODevice
from PyQt5.QtNetwork import QTcpSocket

from source.message import Message, Mode


class Client(QThread):
    need_socket = pyqtSignal()
    def __init__(self, descriptor, server):
        super().__init__()
        self.socketDescriptor = descriptor
        socket = QTcpSocket()
        socket.setSocketDescriptor(descriptor)
        self.ip = socket.peerAddress().toString()[7:]
        self.port = socket.peerPort()
        self.server = server
        # self.socket.nextBlockSize = 0
        # self.socket.readyRead.connect(self.recieve)

    def run(self):
        socket = QTcpSocket()
        socket.open(QIODevice.ReadWrite)
        socket.setSocketDescriptor(self.socketDescriptor)
        socket.readyRead.connect(lambda: self.recieve(socket))
        socket.disconnected.connect(self.server.remove_dead_connection)
        socket.disconnected.connect(socket.disconnected)
        self.need_socket.connect(lambda: self.write(socket))
        self.exec_()

    def connect(self):
        self.socket[0].connectToHost(self.ip, self.port)


    def recieve(self, socket):
        data = socket.readAll()
        index = self.get_spec_symbol_index(data)
        size = int(data[:index])
        data = data[index + 1:]
        while data.size() < size:
            socket.waitForReadyRead()
            data.append(socket.readAll())
        data = bytes(data)
        if len(data) > 0:
            message = self.try_get_message(data)
            if message is None:
                return
            self.choose_action(message)

    def choose_action(self, message):
        if message.mode == Mode.Normal or message.mode == Mode.File:
            self.server.add_new_message(message)
        elif message.mode == Mode.Online:
            self.server.update_online(message)
        elif message.mode == Mode.Neighb:
            self.server.peer_manager.add_client(message)

    def send(self, message):
        data = Message.to_bytes(message)
        data = self.server.cryptographer.encrypt(data, message.to)
        if not data:
            return
        self.bytes = bytes(str(len(data)) + '\n', encoding='utf-8')
        self.data = data
        self.need_socket.emit()
        # socket.write(bytes(str(len(data)) + '\n', encoding='utf-8'))
        # socket.write(data)

    def write(self, socket):
        socket.write(self.bytes)
        socket.write(self.data)

    def try_get_message(self, bytes):
        keys = ['all', self.server.client_info.name]
        for key in keys:
            decrypted = self.server.cryptographer.decrypt(bytes, key)
            try:
                return Message.from_bytes(decrypted)
            except OverflowError:
                continue
            except PickleError:
                continue
        return None

    def get_spec_symbol_index(self, bytes):
        for i in range(len(bytes)):
            if ord(bytes[i]) == 10:
                return i
