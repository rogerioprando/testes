import socket
import re
from multiprocessing import Process, Queue, Manager

UDP_PORT = 4047



class SocketServer:

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self):
        self.request_queue = Queue()     # fila para receber os comandos dos clientes (testar o recebimento de tupla)
        self.socketsend_queue = Queue()  # fila de envio
        self.socketrecv_queue = Queue()  # fila de recebimento
        self.devices_list = {}
        self.addr_device = ()

    def init_queues(self):
        receiver_process = Process(target=self.receiving, args=(self, self.sock))
        sender_process = Process(target=self.sending, args=(self, self.sock))
        receiver_process.start()
        sender_process.start()

    @staticmethod
    def receiving(self, sock):
        sock.bind(('', UDP_PORT))
        while True:
            data, addr = sock.recvfrom(1024)
            data = data.decode('ascii')
            self.addr_device = addr
            print('\n\n')
            print('[RECV] Recebido {} de {}' .format(data, addr))
            self.answer_ack(self, data)
            # se e kp adiciona no dict, caso contrario o evento sera processado
            if self.iskeepalive(data):
                id = re.findall(r'\w[^;ID=\r]+', data)
                self.devices_list[str(id[1])] = addr
                print('ID: {} e IP {}' .format(id[1], addr))

    @staticmethod
    def sending(self, sock):
        print('[SEND]')
        while True:
            msg = self.socketsend_queue.get()
            print('msg .get(): {}' .format(msg))
            print('self.addr_device {}' .format(self.addr_device))
            #sock.sendto(msg.encode(), (self.addr_device[0],self.addr_device[1]))
            #sock.sendto((msg+'\r\n').encode(), (DEVICE_IP, 4095))
            print('[SEND] Enviado {} para {}' . format(msg, self.addr_device))

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
        print(ack)
        self.socketsend_queue.put(ack)

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