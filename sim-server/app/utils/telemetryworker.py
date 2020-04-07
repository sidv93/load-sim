import threading
import time

class TelemetryWorker(threading.Thread):

    def __init__(self, id, pumprate=1, growthrate=1):
        threading.Thread.__init__(self)
        self.__stop = threading.Event()
        self.__lock = threading.RLock()

        self.__id = id
        self.__pumprate = pumprate
        self.__growthrate = growthrate
        self.__data = {
            'id': id,
            'val': 0
        }
    
    def id(self):
        return self.__id

    def stop(self):
        self.__stop.set()

    def stopped(self):
        return self.__stop.isSet()

    def data(self):
        return self.__data

    def run(self):
        self.__lock.acquire()
        self.pumpdata()
        self.__lock.release()

    def pumpdata(self):
        while not self.stopped():
            time.sleep(self.__pumprate)
            self.__data['val'] += self.__growthrate