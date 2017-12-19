import unittest

from PyQt5.QtNetwork import QTcpServer, QHostAddress, QTcpSocket


class TestClient(unittest.TestCase):
    def test_connect(self):
        server = QTcpServer()
        server.listen(QHostAddress.Any, 12345)
        socket = QTcpSocket()
        socket.bind()
        socket.readAll()