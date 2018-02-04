from SocketServer import *


if __name__ == '__main__':
    conect_xvm = SocketServer()
    conect_xvm.init_queues()
    while True:
        id = input('[MAIN] ID: \n').strip()
        msg = input('[MAIN] MSG: \n').strip()
        data_send = (msg, id)
        conect_xvm.socketsend_queue.put(data_send)