
import re
import hashlib

def main():
    b = 'gur2001'
    print hashlib.md5(b).hexdigest() == hashlib.md5('gur2001').hexdigest()
    print hashlib.md5(b).hexdigest()


















if __name__ == '__main__':
    main()




"""
from server_class import Server_management

import time
import threading

SERVER_OBJECT = Server_management()



class StoppableThread(threading.Thread):

    def __init__(self):
        super(StoppableThread, self).__init__()
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def stopped(self):
        return self.stop_event.is_set()

    def run(self):
        while not self.stopped():
            try:
                print 'hello'
                time.sleep(1)
                a = 1 / 0
            except:
                if not self.stopped():
                    print 'stopped in'
                    self.stop()
                break
        print '1234'

def main():

    s = StoppableThread()
    s.start()
    time.sleep(5)
    if not s.stopped():
        print 'stopped out'
        s.stop()
    s.join()











if __name__ == '__main__':
    main()
"""