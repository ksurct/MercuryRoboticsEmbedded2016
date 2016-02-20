# from .hardware.parts import RobotBase, LED, Motor
from contextlib import suppress
import asyncio
import signal

from .hardware.wiringpi_parts import (
    WPRobotBase as RobotBase,
    WPLED as LED,
    WPMotor as Motor,
    WPSpeedEncoder as SpeedEncoder
)
from .protocol.server import Server as server_base
from .protocol.server2 import ClientlessWebSocketServer
from .process_setup import process_setup
from .controller import Controller


class Robot(RobotBase):
    def __init__(self):
        super().__init__()
        self.head_lights = self.attach_device(LED(6))
        self.motor_left = self.attach_device(Motor(20, 19, 18))
        self.motor_left_speed = self.attach_device(SpeedEncoder(22, 21))
        self.motor_right = self.attach_device(Motor(17, 16, 13))
        self.motor_right_speed = self.attach_device(SpeedEncoder(24, 23))

Server = lambda: server_base(8002)


def main():
    process_setup()

    with Robot() as robot:
        server = ClientlessWebSocketServer(8002)
        loop = asyncio.get_event_loop()
        controller = Controller(loop, robot, server)

        # loop.add_signal_handler(signal.SIGINT, loop.close)
        loop.run_until_complete(server.start_server())
        loop.run_until_complete(controller.run())
        loop.run_forever()
