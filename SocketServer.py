import socket
import re
from multiprocessing import Process, Queue, Manager

UDP_PORT = 4047


class SocketServer:

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self):
        self.request_queue = Queue()     # fila para receber os comandos dos clientes (testar o recebimento de tupla)
        self.socketsend_queue = Queue()  # fila de envio (sempre com uma tupla)
        self.socketrecv_queue = Queue()  # fila de recebimento (qualquer coisa)
        self.num_sequence = 1            # sequencia das mensagens 0001 a 7FFF (hexadecimal)
        self.manager = Manager()
        self.addr_devices_list = self.manager.dict()

    def init_queues(self):
        receiver_process = Process(target=self.receiving, args=(self, self.sock, self.addr_devices_list))
        sender_process = Process(target=self.sending, args=(self, self.sock, self.addr_devices_list))
        receiver_process.start()
        sender_process.start()

    @staticmethod
    def receiving(self, sock, devices_addrs):
        sock.bind(('', UDP_PORT))
        while True:
            data, addr = sock.recvfrom(1024)
            data = data.decode('ascii')
            print('\n\n')
            print('[RECV] Recebido {} de {}' .format(data, addr))
            id = re.findall(r'ID=([A-F0-9]{4})', data)
            devices_addrs[str(id[0])] = addr
            self.answer_ack(self, data)
            if not self.iskeepalive(data):
                self.socketrecv_queue.put(data)

    @staticmethod
    def sending(self, sock, devices_addrs):
        while True:
            to_send = self.socketsend_queue.get()   # to_send[0]: data to_send[1]: id
            if bool(devices_addrs.get(to_send[1])):
                sock.sendto((to_send[0] + '\r\n').encode(), devices_addrs[to_send[1]])
                # essa linha localhost usa apenas quando for testar sem virloc
                # sock.sendto((msg[0] + '\r\n').encode(), ('localhost', 4095))
                print('[SEND] Enviado {} para {}'.format(to_send, devices_addrs[to_send[1]]))
            else:
                print('[SEND] ID {} não possui um IP' .format(to_send[1]))

    @staticmethod
    def iskeepalive(data):
        prefix = re.findall(r'\w[^,\r]+', data)
        if prefix[0] == 'RUS04':
            return True
        else:
            return False

    @staticmethod
    def answer_ack(self, data):
        default = '>ACK;ID={id};#{seq};*{crc}<'
        seq = re.findall(r'\w[^;\r]+', data)
        id = re.findall(r'ID=([A-F0-9]{4})', data)
        ack = default.format(id=id[0], seq=seq[2], crc=0)
        crc = hex(self.calcula_crc(ack))[2:].upper()
        ack = default.format(id=id[0], seq=seq[2], crc=str(crc))
        tuple_ack = (ack, id[0])
        self.socketsend_queue.put(tuple_ack)

    @staticmethod
    def calcula_crc(data):
        crc = 0
        for ch in data:
            if ch == '*':
                break
            else:
                ch = ord(ch)
                crc = crc ^ ch
        return crc

    def sendcommand(self, data):
        default = '>{cmd};ID={id};#{seq};*{crc}<'
        cmd, id = data
        send = default.format(cmd=str(cmd).upper(), id=id, seq=str(hex(self.num_sequence))[2:].upper().zfill(4), crc=0)
        crc = hex(self.calcula_crc(send))[2:].upper().zfill(2)
        send = default.format(cmd=str(cmd).upper(), id=id, seq=str(hex(self.num_sequence))[2:].upper().zfill(4), crc=str(crc))
        to_send = send, id
        self.socketsend_queue.put(to_send)
        if self.num_sequence < 32767:
            self.num_sequence = self.num_sequence + 1
        else:
            self.num_sequence = 1