from pickle import PickleError

from PyQt5.QtCore import QObject

from source.message import Message, Mode


class Client(QObject):
    def __init__(self, ip, port, socket, server):
        super().__init__()
        self.ip = ip
        self.port = port
        self.socket = socket
        self.server = server
        self.socket.nextBlockSize = 0
        self.socket.readyRead.connect(self.recieve)

    def connect(self):
        self.socket.connectToHost(self.ip, self.port)

    def recieve(self):
        data = self.socket.readAll()
        index = self.get_spec_symbol_index(data)
        size = int(data[:index])
        data = data[index + 1:]
        while data.size() < size:
            self.socket.waitForReadyRead()
            data.append(self.socket.readAll())
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
        self.socket.write(bytes(str(len(data)) + '\n', encoding='utf-8'))
        self.socket.write(data)

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
