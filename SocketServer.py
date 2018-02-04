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
            id = re.findall(r'\w[^;ID=\r]+', data)
            devices_addrs[str(id[1])] = addr
            self.answer_ack(self, data)
            if not self.iskeepalive(data):
                self.socketrecv_queue.put(data) # coloca evento recebido na fila

    @staticmethod
    def sending(self, sock, devices_addrs):
        while True:
            msg = self.socketsend_queue.get()
            print('[SEND] .get() msg: {} id: {}' .format(msg[0], msg[1]))
            sock.sendto((msg[0]+'\r\n').encode(), devices_addrs[msg[1]])
            sock.sendto((msg[0] + '\r\n').encode(), ('localhost', 4095))
            print('[SEND] Enviado {} para {}' . format(msg, devices_addrs[msg[1]]))

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
        seq = re.findall(r'\w[^;\r]+', data) #seq[2]
        id = re.findall(r'\w[^;ID=\r]+', data) #id[1]
        #print('seq {} id {}'.format(seq[2], id[1]))
        ack = default.format(id=id[1], seq=seq[2], crc=0)
        crc = hex(self.calcula_crc(ack))[2:].upper()
        ack = default.format(id=id[1], seq=seq[2], crc=str(crc))
        tuple_ack = (ack, id[1])
        #print('[ANS ACK] tuple ack: {}' .format(tuple_ack))
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
