import datetime
import socket
import re


# UDP_IP = 'localhost'
UDP_PORT = 4047

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", UDP_PORT))

def SendCMD():
    #>QGV;ID=4116;#8058;*51<
    cmd = '>QGV;ID=4116;#8058;*51<'
    return cmd

def SendACK():
    # >ACK;ID=4116;#802B;*25<
    ack = '>ACK;ID={id};#{n};*{crc}<'
    ack_format = ack.format(id=e1.id, n=e1.seq, crc=00)
    crc = hex(calcula_crc(ack_format))[2:].upper()
    ack_format = ack.format(id=e1.id, n=e1.seq, crc=str(crc))
    return ack_format


# Calculate CRC
def calcula_crc(data):
    crc = 0
    for ch in data:
        if ch == '*':
            break
        else:
            ch = ord(ch)
            crc = crc ^ ch
    return crc

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


if __name__ == '__main__':
    while True:
        data, addr = sock.recvfrom(1024)  # recebe mensagem
        data_format = data.decode('ascii')  # transforma em ascii
        e1 = Event()
        e1.dataxvm = data_format
        e1.parser()
        sock.sendto(SendACK().encode(), (addr[0], addr[1]))
        #sock.sendto(SendCMD().encode(), (addr[0], addr[1]))
        #sock.settimeout(2)

        print("received message: {} at {} from {} {}".format(data.decode('ascii'), datetime.datetime.now(), addr[0], addr[1]))

        print("\n")
        print("XVM: {}".format(e1.dataxvm))
        print("EVENTO: {}".format(e1.get_event()))
        print("ID: {}".format(e1.get_id()))
        print("SEQ: {}".format(e1.get_seq()))
        print("CRC: {}".format(e1.get_crc()))
        print("ACK to send: {}".format(SendACK()))

        """
        # parser do evento recebido
        #data_parser = re.findall(r'\w[^;\s<ID=]+',data_format)
        data_parser = re.findall(r'\w[^;\r]+',data_format) # regex pacote principal
        event = data_parser[0]
        id_msgn = data_parser[1]
        n_msgn = data_parser[2]
        crc_msgn_recv = data_parser[3]
        print(data_parser, event, id_msgn, n_msgn, crc_msgn_recv)
        # regex ID: \w[^=]+
        # regex Evento: \w[^,]+
        # regex CRC: \w[^<]+
    
        ack_format = ack.format(id=id_msgn, n=n_msgn, crc=crc_msgn_send)
        crc_msgn_send = calcula_crc(ack_format)
        ack_format = ack.format(id=id_msgn, n=n_msgn, crc=str(hex(crc_msgn_send)[2:]).upper())
        print(ack_format)
        print("Resposta ACK: {}" .format(ack_format))
        print("CRC da resposta (INT): {}" .format(crc_msgn_send))
        print("CRC da resposta (HEX): {}" .format(hex(crc_msgn_send)))
        sock.sendto(ack_format.encode(), (addr[0], addr[1]))
    
        """
        # resposta ack






