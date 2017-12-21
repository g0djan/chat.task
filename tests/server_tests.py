import unittest

import time
from unittest.mock import patch

from PyQt5.QtNetwork import QTcpSocket

from source.chat_window import ChatWindow
from source.client import Client
from source.client_info import ClientInfo
from source.message import Message, Mode, MessageInfo
from source.server import Server


class ServerTest(unittest.TestCase):
    def test_add_client_to_connections(self):
        # arrange
        with patch('source.server.Server') as mock:
            server = Server('dude', 666, mock)
        client = Client('127.0.0.1', 666, QTcpSocket(), server)

        # act
        server.add_client(client)

        # assert
        self.assertEqual(server.connections[client.ip], client)

    def test_add_message_new_will_be_added(self):
        # arrange
        with patch('source.server.Server') as mock:
            server = Server('dude', 666, mock)
        message = Message('127.0.0.1', 'good news', Mode.Normal)

        # act
        server.add_new_message(message)

        # assert
        self.assertTrue(MessageInfo(message) in server.stored_messages)

    def test_add_message_old_wont_call_has_new_message(self):
        # arrange
        with patch('source.server.Server') as mock:
            server = Server('dude', 666, mock)
        message = Message('127.0.0.1', 'good news', Mode.Normal)
        server.stored_messages.add(MessageInfo(message))
        flag = False

        def change_flag():
            nonlocal flag
            flag = not flag

        server.has_new_message.connect(change_flag)

        # act
        server.add_new_message(message)

        # assert
        self.assertFalse(flag)

    def test_remove_from_online(self):
        # arrange
        with patch('source.server.Server') as mock:
            server = Server('dude', 666, mock)
        ip = '127.0.0.1'
        server.online[ip] = server.client_info
        message = Message(ip, ip, Mode.Offline)

        # act
        server.remove_from_online(message)

        # assert
        self.assertFalse(ip in server.online)

    def test_update_online_when_new_ip(self):
        # arrange
        with patch('source.server.Server') as mock:
            server = Server('dude', 666, mock)
        ip = '127.0.0.1'
        message = Message(ip, server.client_info, Mode.Online)

        # act
        server.update_online(message)

        # assert
        self.assertEqual(server.online[ip], server.client_info)

    def test_update_online_when_actual_info(self):
        # arrange
        with patch('source.server.Server') as mock:
            server = Server('dude', 666, mock)
        ip = '127.0.0.1'
        old_client_info = ClientInfo('dude', ip, len(server.connections))
        time.sleep(1)
        new_client_info = ClientInfo('dude', ip, len(server.connections))
        server.online[ip] = old_client_info
        message = Message(ip, new_client_info, Mode.Online)

        # act
        server.update_online(message)

        # assert
        self.assertNotEqual(server.online[ip], old_client_info)

    def test_update_client_info(self):
        # arrange
        with patch('source.server.Server') as mock:
            server = Server('dude', 666, mock)
        client = Client('127.0.0.1', 666, QTcpSocket(), server)
        server.connections[client.ip] = client

        # act
        server.update_client_info()

        # assert
        self.assertEqual(server.client_info.incidents_cnt, 1)

    def test_merge_online_when_new_ip(self):
        # arrange
        with patch('source.server.Server') as mock:
            server = Server('dude', 666, mock)
        ip = '127.0.0.1'
        online = {ip: server.client_info}
        message = Message(ip, online, Mode.Neighb)

        # act
        server.merge_online(message)

        # assert
        self.assertTrue(ip in server.online)

    def test_merge_online_when_actual_info(self):
        # arrange
        with patch('source.server.Server') as mock:
            server = Server('dude', 666, mock)
        ip = server.client_info.ip
        old_client_info = ClientInfo('dude', ip, len(server.connections))
        time.sleep(1)
        new_client_info = ClientInfo('dude', ip, len(server.connections))
        server.online[ip] = old_client_info
        online = {server.client_info.ip: new_client_info}
        message = Message(ip, online, Mode.Neighb)

        # act
        server.merge_online(message)

        # assert
        self.assertEqual(server.online[ip], new_client_info)
