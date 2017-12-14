from datetime import datetime
from enum import Enum

import pickle


class Mode(Enum):
    Normal = 1
    Online = 2
    Neighb = 3
    Offline = 4


class Message:
    def __init__(self, ip, content, mode):
        self.sender_ip = ip
        self.content = content
        self.time = datetime.today()
        self.mode = mode

    @staticmethod
    def to_bytes(message):
        return pickle.dumps(message)

    @staticmethod
    def from_bytes(bytes):
        return pickle.loads(bytes)

    def __eq__(self, other):
        return (self.content, self.time, self.mode) == \
               (other.content, other.time, other.mode)

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.content, self.time, self.mode))
