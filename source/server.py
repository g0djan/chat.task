import socket

from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtNetwork import QTcpServer, QHostAddress

from source.client import Client
from source.cryptographer import Cryptographer
from source.file_worker import FileWorker
from source.message import Message, Mode, MessageInfo
from source.client_info import ClientInfo
from source.peermanager import PeerManager


class Server(QTcpServer):
    has_new_message = pyqtSignal()
    change_connections_cnt = pyqtSignal()

    def __init__(self, name, port, chat_window):
        super().__init__()
        self.chat_window = chat_window
        self.file_worker = FileWorker()
        self.port = port
        self.connections = {}
        self.client_info = ClientInfo(name, self.get_ip(), len(self.connections))
        self.cryptographer = Cryptographer('utf-8', name)
        self.listen(QHostAddress.Any, 12345)
        self.peer_manager = PeerManager(self)
        #self.newConnection.connect(self.add_next_client)
        self.stored_messages = set()
        self.online = {self.client_info.ip: self.client_info}
        self.change_connections_cnt.connect(
            lambda: self.peer_manager.update_connections(self.online))

    def incomingConnection(self, descriptor):
        client = Client(descriptor, self)
        #client.send(Message(self.get_ip(), self.online, Mode.Neighb))
        self.add_client(client)

    # def add_next_client(self):
    #     connection = self.nextPendingConnection()
    #     ip = connection.peerAddress().toString()[7:]
    #     port = connection.peerPort()
    #     client = Client(ip, port, connection, self)
    #     if ip in self.connections:
    #         connection.disconnectFromHost()
    #         return
    #     client.send(Message(self.get_ip(), self.online, Mode.Neighb))
    #     self.add_client(client)

    def add_client(self, client):
        client.socket = [client.start()][0]
        client.start()
        if client.ip in self.connections:
            client.exit(0)
            #client.socket.disconnectFromHost()
            return
        #client.socket.disconnected.connect(lambda: self._remove_dead_connection(client))
        self.connections[client.ip] = client
        client.send(Message(self.get_ip(), self.online, Mode.Neighb))
        self.change_connections_cnt.emit()
        self.chat_window.refresh_online_and_connections(self.online, self.connections)

    def add_new_message(self, message):
        info = MessageInfo(message)
        if info not in self.stored_messages:
            self.last_message = message
            self.stored_messages.add(info)
            self.has_new_message.emit()
            if message.sender_ip != self.client_info.ip and message.mode == Mode.File:
                folder = self.chat_window.get_folder()
                if folder:
                    self.file_worker.save_file(folder, message.content)
                else:
                    del message

    def send_all(self, message):
        for key in self.connections:
            self.connections[key].send(message)

    def resend(self):
        self.send_all(self.last_message)

    def remove_dead_connection(self, client):
        self.connections.pop(client.ip)
        if client.ip in self.online:
            self.chat_window.say_he_is_offline(self.online[client.ip].name)
            self.online.pop(client.ip)
        message = Message(self.get_ip(), client.ip, Mode.Offline)
        self.send_all(message)
        self.change_connections_cnt.emit()
        self.chat_window.refresh_online_and_connections(self.online, self.connections)

    def remove_from_online(self, message):
        if message.content in self.online:
            self.chat_window.say_he_is_offline(self.online[message.content].name)
            self.online.pop(message.content)
            self.send_all(message)
        self.chat_window.refresh_online_and_connections(self.online, self.connections)

    def get_ip(self):
        return socket.gethostbyname(socket.gethostname())

    def update_online(self, message):
        ip = message.sender_ip
        new_time = message.content.update_time
        new_message = ip in self.online and new_time > self.online[ip].update_time
        if ip not in self.online:
            self.chat_window.say_he_is_online(message.content.name)
        if ip not in self.online or new_message:
            self.online[ip] = message.content
            self.send_all(message)
            self.peer_manager.update_connections(self.online)
        self.chat_window.refresh_online_and_connections(self.online, self.connections)

    def update_client_info(self):
        self.client_info.update_incidents_cnt(len(self.connections))
        ip = self.get_ip()
        message = Message(ip, self.client_info, Mode.Online)
        self.send_all(message)
        self.chat_window.refresh_online_and_connections(self.online, self.connections)

    def merge_online(self, message):
        online = message.content
        for ip in online:
            if ip not in self.online:
                self.chat_window.say_he_is_online(online[ip].name)
            if ip not in self.online or online[ip].update_time > self.online[ip].update_time:
                self.online[ip] = online[ip]
        self.peer_manager.update_connections(self.online)
        self.chat_window.refresh_online_and_connections(self.online, self.connections)
