from logging import getLogger
from time import time, sleep
from threading import Thread, Lock

BUFFER_SIZE = 5
UPDATE_RATE = .2

logger = getLogger(__name__)


class DistanceThread(object):
    def __init__(self, robot):
        self.robot = robot
        self.running = False
        self.lock = Lock()
        self.thread = Thread(target=self._run)
        self.last_time = 0

    def __enter__(self):
        self.running = True
        self.thread.start()
        return self

    def __exit__(self, *enc):
        self.running = False
        self.thread.join()
        pass

    def get(self):
        with self.lock:
            return 0

    def update(self):
        print('foo')

    def _run(self):
        while self.running:
            sleep(UPDATE_RATE)
            self.update()


if __name__ == '__main__':
    t = DistanceThread()

    with t:
        sleep(1)
