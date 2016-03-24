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
from .hardware.spidev_parts import DistanceSensor
from .hardware.servo import Servo
from .protocol.server import Server as server_base
from .protocol.server2 import ClientlessWebSocketServer
from .process_setup import process_setup
from .controller import Controller
from .util import AsyncioLoop, get_config


class Robot(RobotBase):
    def __init__(self):
        super().__init__()
        self.head_lights = self.attach_device(LED(6))
        self.motor_left = self.attach_device(Motor(20, 19, 18))
        self.motor_left_speed = self.attach_device(SpeedEncoder(22, 21))
        self.motor_right = self.attach_device(Motor(17, 16, 13))
        self.motor_right_speed = self.attach_device(SpeedEncoder(24, 23))
        self.camera = self.attach_device(Servo(0, 0))
        self.launch = self.attach_device(Servo(0, 0))
        self.claw  = self.attach_device(Servo(0, 0))
        self.dist_fr = self.attach_device(DistanceSensor(0))
        self.dist_fl= self.attach_device(DistanceSensor(0))
        self.dist_br = self.attach_device(DistanceSensor(0))
        self.dist_bl = self.attach_device(DistanceSensor(0))


def main():
    config = get_config()
    process_setup()

    with Robot() as robot:
        server = ClientlessWebSocketServer(config.port)
        loop = asyncio.get_event_loop()
        controller = Controller(loop, robot, server)

        with AsyncioLoop() as loop:
            loop.submit(server.start_server())
            loop.submit(controller.run())
