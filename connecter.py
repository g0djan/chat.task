from PyQt5.QtNetwork import QTcpSocket


class Connecter:
    def __init__(self, server):
        self.server = server

    def set_connection(self, socket, ip, port):
        connected = socket.state() == QTcpSocket.ConnectedState
        if connected:
            self.share_data()
            return True
        else:
            socket.connected.connect(self.share_data)
            socket.connectToHost(ip, port)

    def share_data(self):
        pass