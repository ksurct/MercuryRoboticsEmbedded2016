import spidev
from contextlib import ExitStack
from collections import deque
from threading import Lock
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from logging import getLogger

logger = getLogger(__name__)

BUFFER_SIZE = 10
BUFFER_UPDATE = .3


class DistanceSensor(object):
    def __init__(self, channel):
        self.channel = channel
        self.spi = None
        self.buffer = deque([0] * BUFFER_SIZE, maxlen=BUFFER_SIZE)
        self.executer = None
        self.context = ExitStack()
        self.lock = Lock()

    def __enter__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        self.executer = ThreadPoolExecutor(1)
        self.context.enter_context(self.executer)
        self.executer.submit(self.run_sample)
        return self

    def __exit__(self, *enc):
        self.spi = None
        self.executer = None
        self.context.close()

    def run_sample(self):
        try:
            while self.executer:
                sleep(BUFFER_UPDATE)
                self.sample()
        except Exception as e:
            logger.exception('Thread failure')
            exit()

    def sample(self):
        with self.lock:
            self.buffer.append(self.get_raw())

    def get_raw(self):
        data = self.spi.xfer2([1,(8+self.channel)<<4,0])
        return data

    def get(self):
        with self.lock:
            return sum(self.buffer) / BUFFER_SIZE


if __name__ == '__main__':
    with DistanceSensor(0) as f:
        while True:
            sleep(1)
            print(f.get_clean())
