import socket
from multiprocessing import Process, Queue, Manager


UDP_PORT = 4047

DEVICE_IP = '152.252.114.050'

#>QGV;ID=4116;#829A;*26<


def receive(sock, output_queue, devices):
    while True:
        print("[TH_RECV] sock.recvfrom \n")
        data, addr = sock.recvfrom(1024)  # recebe mensagem
        print('[TH_RECV] recebido %s de %s' % (data, addr))
        data_format = data.decode('ascii')  # transforma em ascii
        output_queue.put(data_format)
        print("[TH_RECV] RESPOSTA: %s \n" % data_format)
        devices['4116'] = addr
        print("[TH_RECV] devices_map: %s " % devices)
        print("[TH_RECV] devices_map 2: ", devices['4116'])


def send(sock, input_queue, devices):
    while True:
        message = input_queue.get()
        print("[TH_SEND] sock.sendto \n")
        print("[TH_SEND] devices_map 2: ", devices['4116'])
        sock.sendto((message+'\r\n').encode(), (devices['4116'][0], devices['4116'][1]))
        #sock.settimeout(2)


if __name__ == '__main__':
    work_queue = Queue()
    result_queue = Queue()

    manager = Manager()
    devices_maplist = manager.dict()
    devices_maplist.update({'4116': ('ip aqui', 12345)})

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', UDP_PORT))

    worker_receive = Process(target=receive, args=(sock, result_queue, devices_maplist))
    worker_receive.start()

    worker_send = Process(target=send, args=(sock, work_queue,devices_maplist))
    worker_send.start()


    while True:
        print("[WH MAIN] devices_map: %s " % devices_maplist)
        print("[WH MAIN] RESPOSTA: %s \n" % result_queue.get())
        cmd = input('[WH MAIN] Comando: \n').strip()
        work_queue.put(cmd)