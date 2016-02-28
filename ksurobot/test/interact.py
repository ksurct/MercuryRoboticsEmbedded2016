import asyncio
import websockets
from contextlib import ExitStack

from ptpython.repl import embed

from ..protocol.proto import main_pb2
from ..robot import Robot, Server


def main():
    with ExitStack() as e:
        r = Robot()
        e.enter_context(r)
        # s = Server()
        # e.enter_context(s)
    # ws = Websocket()
        embed(globals(), locals())


if __name__ == '__main__':
    main()
