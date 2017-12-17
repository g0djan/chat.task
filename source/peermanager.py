from PyQt5.QtNetwork import QTcpSocket

from source.client import Client
from source.message import Message, Mode

OPTIMAL_CONNECT_NUMBER = 3

PORT = 12345


class PeerManager:
    def __init__(self, server):
        self.server = server

    def update_connections(self, online):
        if len(self.server.connections) >= OPTIMAL_CONNECT_NUMBER:
            return
        online = list(map(lambda key: (key, online[key].incidents_cnt), online))
        online.sort(key=lambda x: x[1])
        i = 0
        online_cnt = len(online)
        while i < online_cnt and len(self.server.connections) < OPTIMAL_CONNECT_NUMBER:
            ip = online[i][0]
            if ip != self.server.get_ip() and ip not in self.server.connections:
                self.set_connection(ip, self.server.port)
            i += 1
        self.server.update_client_info()

    def set_connection(self, ip, port):
        socket = QTcpSocket()
        self.last_client = Client(ip, port, socket, self.server)
        socket.connected.connect(self._share_data)
        self.last_client.connect()

    def add_client(self, message):
        if message.mode == Mode.Neighb and message.sender_ip not in self.server.connections:
            self.server.add_client(self.last_client)
            self.server.merge_online(message)

    def _share_data(self):
        self.last_client.socket.connected.disconnect(self._share_data)
        if len(self.server.connections) >= OPTIMAL_CONNECT_NUMBER:
            self.last_client.socket.disconnectFromHost()
            return
        if self.last_client.ip in self.server.connections:
            self.last_client.socket.disconnectFromHost()
            return
        message = Message(self.server.get_ip(), self.server.online, Mode.Neighb)
        self.last_client.send(message)
