import socket, time

UDP_IP = 'localhost'
UDP_PORT = 4047

msg_rax = '>RAX11,00480,261017154156-2747317-04841725032203,20449;ID=4089;#5B77;*3A<'
msg_kp1 = '>RUS04,;ID=4001;#5B77;*3A<'
msg_kp2 = '>RUS04,;ID=4002;#5B77;*3A<'
msg_kp3 = '>RUS04,;ID=4003;#5B77;*3A<'
msg_kp4 = '>RUS04,;ID=4004;#5B77;*3A<'
msg_ruv = '>RUV1092,;ID=1018;#768C;*13<'
msg_rus = '>RUS00,261017153234-2254941-04530492057300,26642;ID=1223;#5870;*4E<'
cmd = ''
id = 50
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while cmd != 'exit':
    cmd = input('\n cmd: ').strip()
    if cmd == 'rax':
        message = msg_rax
    elif cmd == 'kp1':
        message = msg_kp1
    elif cmd == 'kp2':
        message = msg_kp2
    elif cmd == 'kp3':
        message = msg_kp3
    elif cmd == 'kp4':
        message = msg_kp4
    elif cmd == 'ruv':
        message = msg_ruv
    elif cmd == 'rus':
        message = msg_rus
    else:
        message = msg_rus
    print(message)
    sock.sendto(message.encode(), (UDP_IP, UDP_PORT))

while True:
    msg_kp2 = '>RUS04,MESSAGE_ERROR;ID='+str(id)+';#5B77;*3A<'
    sock.sendto(msg_kp2.encode(), (UDP_IP, UDP_PORT))
    print(id)
    id = id + 1
    time.sleep(0.01)

