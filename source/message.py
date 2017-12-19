import pickle
from datetime import datetime
from enum import Enum


class Mode(Enum):
    Normal = 1
    Online = 2
    Neighb = 3
    Offline = 4
    File = 5


class Message:
    def __init__(self, ip, content, mode, to='all'):
        self.sender_ip = ip
        self.content = content
        self.time = datetime.today()
        self.mode = mode
        self.to = to

    @staticmethod
    def to_bytes(message):
        return pickle.dumps(message)

    @staticmethod
    def from_bytes(bytes):
        return pickle.loads(bytes)


class MessageInfo:
    def __init__(self, message):
        self.sender_ip = message.sender_ip
        self.time = message.time
        self.mode = message.mode
        self.to = message.to

    def __eq__(self, other):
        return (self.sender_ip, self.time, self.mode, self.to) == \
               (other.sender_ip, other.time, other.mode, other.to)

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.sender_ip, self.time, self.mode, self.to))
