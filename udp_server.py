import socket

UDP_IP = 'localhost'
UDP_PORT = 4095

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)
    _data = data.decode('ascii')
    print(data.decode('ascii'))
