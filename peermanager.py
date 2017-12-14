from PyQt5.QtNetwork import QTcpSocket

from client import Client
from message import Message, Mode

OPTIMAL_CONNECT_NUMBER = 4

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
        self.server._update_client_info()

    def set_connection(self, ip, port):
        socket = QTcpSocket()
        self.last_client = Client(ip, port, socket, self.server)
        socket.connected.connect(self.share_data)
        # socket.readyRead.connect(self.add_client)
        self.last_client.connect()

    def share_data(self):
        self.last_client.socket.connected.disconnect(self.share_data)
        if len(self.server.connections) >= OPTIMAL_CONNECT_NUMBER:
            self.last_client.socket.disconnectFromHost()
            return
        if self.last_client.ip in self.server.connections:
            self.last_client.socket.disconnectFromHost()
            return
        message = Message(self.server.get_ip(), self.server.online, Mode.Neighb)
        self.last_client.send(message)


    def add_client(self, message):
        # message = self.last_client.recieve()  # TODO: change recieve
        if message.mode == Mode.Neighb and message.sender_ip not in self.server.connections:
            self.server.add_client(self.last_client)
            self.server.merge_online(message)  # TODO: check and repair method maybe it should be merge with time
        # self.last_client.socket.readyRead.disconnect(self.add_client)
