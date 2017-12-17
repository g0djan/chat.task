import unittest

from PyQt5.QtNetwork import QTcpSocket

from source.message import Message, Mode
from source.server import Server
from source.client import Client


class TestPeerManager(unittest.TestCase):
    def setUp(self):
        # arrange
        self.ip = '127.0.0.1'
        self.port = 666
        self.server = Server('dude', self.port)
        self.client = Client(self.ip, self.port, QTcpSocket(), self.server)
        self.server.peer_manager.last_client = self.client
        self.online = {self.ip: self.server.client_info}
        self.message = Message(self.ip, self.online, Mode.Neighb)

    def test_add_client_change_connetions(self):
        # act
        self.server.peer_manager.add_client(self.message)

        # assert
        self.assertTrue(self.ip in self.server.connections)

    def test_add_client_change_online(self):
        # act
        self.server.peer_manager.add_client(self.message)

        # assert
        for key in self.online.keys():
            self.assertTrue(key in self.server.online.keys())
