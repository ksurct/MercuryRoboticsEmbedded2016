import asyncio
import websockets
from contextlib import ExitStack

from ptpython.repl import embed

from ..protocol.proto import main_pb2
from ..robot import Robot


def set_motor(r, v):
    r.motor_right.set(v)
    r.motor_left.set(v)


def set_motor_rpm(r, v):
    r.motor_left_driver.set(v)
    r.motor_left_driver.set(v)


def interact():
    while True:
        cmd = int(input())
        set_motor(cmd)


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
