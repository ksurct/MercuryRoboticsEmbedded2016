import asyncio
import websockets
from threading import Thread Event
from queue import Queue
from ctypes import c_bool
from multiprocessing import Value
import logging
from concurrent.futures import ThreadPoolExecutor
from contextlib import ExitStack, contextmanager

from .proto import main_pb2

logger = logging.getLogger(__name__)


# class Server(object):
#     def __init__(self, port, loop=None):
#         self.queue = Queue()
#         self.port = port
#         self.websocket = WebsocketsServer(self.queue, self.port)
#
#     def __enter__(self):
#         self.websocket.start()
#         return self
#
#     def __exit__(self, *enc):
#         self.websocket.stop()
#
#     def parse_message(self, msg):
#         return main_pb2.Robot.ParseFromString(msg)
#
#     def serialize_message(self, msg):
#         return main_pb2.BaseStation.SerializeToString()
#
#     def recv(self):
#         self.queue.get()


class EventLoopThread(object):
    def __init__(self, servers_to_start):
        self.context = None
        self.executor = None
        self.loop = None
        self.servers_to_start = servers_to_start
        self.servers = []

    def __enter__(self):
        self.context = ExitStack()
        self.executor = self.context.enter_context(ThreadPoolExecutor(max_workers=1))
        self.context.enter_context(self.event_loop_context())
        return self

    def __exit__(self, *enc):
        self.context.__exit__(*enc)
        self.context = None
        self.executor = None
        self.loop = None

    def start_loop(self, event):
        logger.info('starting eventloop server')
        loop = asyncio.new_event_loop()
        self.loop = loop
        asyncio.set_event_loop(loop)
        for server_starter in self.servers_to_start:
            server = loop.run_until_complete(server_starter)
            self.servers.append(server)
        loop.call_soon(event.set)
        loop.run_forever()

    def stop_loop(self):
        logger.info('stopping eventloop server')
        self.loop.create_task(self._close_connections())

    @contextmanager
    def event_loop_context(self):
        event = Event()
        event.clear()
        self.executor.submit(self.start_loop, event)
        event.wait()
        logger.info('started eventloop')
        try:
            yield
        finally:
            self.loop.call_soon_threadsafe(self.stop_loop)
            logger.info('stopped eventloop')

    async def _close_connections(self):
        for server in self.servers:
            server.close()
            await server.wait_closed()
        self.loop.stop()


class Server(object):
    def __init__(self, port):
        self.context = None
        self.server = EventLoopThread([self.start_server()])

    def __enter__(self):
        self.context = ExitStack()
        self.context.enter_context(self.server)
        self.context.enter_context(self.event_loop_context())

    def __exit__(self, *enc):
        self.context.__exit__(*enc)

    @asyncio.coroutine
    def time(self, websocket, path):
        import datetime
        import random
        while True:
            now = datetime.datetime.utcnow().isoformat() + 'Z'
            if not websocket.open:
                return
            yield from websocket.send(now)
            yield from asyncio.sleep(random.random() * 3)

    def start_server(self):
        logger.info('starting websockets server')
        start_server = websockets.serve(self.time, '127.0.0.1', 5678)
        # self.server.loop.run_until_complete(start_server)
        return start_server

    @contextmanager
    def event_loop_context(self):
        with ExitStack() as stack:
            # self.server.loop.call_soon_threadsafe(self.start_server)
            yield
