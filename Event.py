import re


class Event():
    dataxvm = ""
    event = ""
    prefix = ""
    id = ""
    seq = ""
    crc = ""

    def __init__(self):
        self.dataxvm = ""
        self.event = ""
        self.prefix = ""
        self.id = ""
        self.seq = ""
        self.crc = ""

    def get_event(self):
        return self.event

    def get_prefix(self):
        return self.prefix

    def get_id(self):
        return self.id

    def get_seq(self):
        return self.seq

    def get_crc(self):
        return self.crc

    def parser(self):
        self.dataxvm = re.findall(r'\w[^;\r]+', self.dataxvm)  # mudar a regex para já deixar os atributos prontos
        self.event = self.dataxvm[0]
        self.prefix = re.findall(r'\w[^,\r]+', self.event)
        self.prefix = self.prefix[0]
        self.id = self.dataxvm[1][3:7]     # melhorar regex
        self.seq = self.dataxvm[2]
        self.crc = self.dataxvm[3][0:2]     # melhorar regex