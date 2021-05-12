import ctypes
import time
from multiprocessing import Process
from multiprocess.managers import Value


def f(name):
    time.sleep(5)
    print('hello', name)

if __name__ == '__main__':
    p = Process(target=f, args=('bob',))
    p.start()
    p.join(timeout=3)
    if p.exitcode != 0:
        print('Timeout')
        p.terminate()
    else:
        print('Job finish')
    time.sleep(8)
    print(p.exitcode)