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
        if self.socket.bytesAvailable() > 0:
            message = Message.from_bytes(self.socket.readAll())
            if message.mode == Mode.Normal:
                self.server.add_new_message(message)
            elif message.mode == Mode.Online:
                self.server.update_online(message)
            elif message.mode == Mode.Neighb:
                self.server.peer_manager.add_client(message)

    def send(self, message):
        bytes = Message.to_bytes(message)
        if not bytes:
            return
        self.socket.write(bytes)
