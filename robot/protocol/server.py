import asyncio
import websockets
from threading import Thread
from queue import Queue
from ctypes import c_bool
from multiprocessing import Value
import logging

from .proto import main_pb2

logger = logging.getLogger(__name__)


class WebsocketsServer(object):
    def __init__(self, queue, port):
        self.queue = queue
        self.port = port
        self.loop = None
        self.thread = None
        self.is_dead = Value(c_bool)

    def start(self):
        self.thread = Thread(target=self.run)
        self.is_dead.value = False
        self.thread.start()

    def run(self):
        with self.is_dead.get_lock():
            if self.is_dead.value:
                return
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            logger.critical('websocket server listening on {}'.format(self.port))
            start_server = websockets.serve(self.handle_connection, 'localhost', self.port)
            self.loop.run_until_complete(start_server)
        self.loop.run_forever()

    def stop(self):
        logger.critical('websocket server shutting down')
        with self.is_dead.get_lock():
            if not self.is_dead.value:
                self.loop.call_soon_threadsafe(self.loop.stop)
            self.is_dead.value = True
        self.thread.join()

    def handle_connection(self, websocket, path):
        while True:
            self.queue.put(websocket.recv())


class Server(object):
    def __init__(self, port, loop=None):
        self.queue = Queue()
        self.port = port
        self.websocket = WebsocketsServer(self.queue, self.port)

    def __enter__(self):
        self.websocket.start()
        return self

    def __exit__(self, *enc):
        self.websocket.stop()

    def parse_message(self, msg):
        return main_pb2.Robot.ParseFromString(msg)

    def serialize_message(self, msg):
        return main_pb2.BaseStation.SerializeToString()

    def recv(self):
        self.queue.get()
