import asyncio
import websockets
from contextlib import ExitStack

from ptpython.repl import embed

from ..protocol.proto import main_pb2
from ..robot import Robot, Server


class Websocket(object):
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.ws = None

    def connect(self):
        self.ws = self.loop.run_until_complete(websockets.connect('ws://localhost:8002/'))

    def send(self, msg):
        assert self.ws, 'Not connected'
        self.loop.run_until_complete(self.ws.send(msg))

    def recv(self):
        self.loop.run_until_complete(self.ws.recv())

    def close(self):
        assert self.ws, 'Not connected'
        self.loop.run_until_complete(self.ws.close())


def main():
    with ExitStack() as e:
        r = Robot()
        e.enter_context(r)
        s = Server()
        e.enter_context(s)
    # ws = Websocket()
        embed(globals(), locals())


if __name__ == '__main__':
    main()
