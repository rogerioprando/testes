import sys
import signal
from multiprocessing import Process, Queue


def upper_caser(input_queue, output_queue):
    message = ''
    try:
        while message != 'quit':
            message = input_queue.get()
            output_queue.put(message.upper())
    except KeyboardInterrupt:
        pass


def do_exit(wq):
    wq.put('quit')
    print("\nGood bye!")
    sys.exit(0)


if __name__ == '__main__':
    result_queue = Queue()
    work_queue = Queue()

    worker = Process(target=upper_caser, args=(work_queue, result_queue))
    worker.start()

    result = ''
    while result != 'QUIT':
        try:
            msg = input('\n> ').strip()
            if len(msg) > 0:
                work_queue.put(msg)
                print(result_queue.get())
        except (EOFError, KeyboardInterrupt):
            do_exit(work_queue)