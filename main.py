from SocketServer import *

if __name__ == '__main__':
    conect_xvm = SocketServer()
    conect_xvm.init_queues()

    while True:
        try:
            id = input('[MAIN] ID: \n').strip()
            msg = input('[MAIN] MSG: \n').strip()
            data_send = (msg, id)
            conect_xvm.sendcommand(data_send)
            rec = conect_xvm.socketrecv_queue.get()
            print(rec)
        except(EOFError, KeyboardInterrupt):
            print('Exit main ...')
            sys.exit(0)
