from datetime import datetime


class ClientInfo:
    def __init__(self, name, ip, incidents_cnt):
        self.name = name
        self.ip = ip
        self.incidents_cnt = incidents_cnt
        self.update_time = datetime.today()

    def update_incidents_cnt(self, incidents_cnt):
        self.incidents_cnt = incidents_cnt
        self.update_time = datetime.today()

    def __eq__(self, other):
        return (self.name, self.ip, self.incidents_cnt) == \
               (other.name, other.ip, other.incidents_cnt)

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash((self.name, self.ip, self.incidents_cnt))
