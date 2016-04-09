from contextlib import suppress
from .controller import Controller
from ..protocol.proto.main_pb2 import Robot as RobotMessage
from ..util import get_config
import asyncio
import websockets
import logging

logger = logging.getLogger(__name__)


class Component(object):
    def __init__(self, **kwargs):
        self.parts = kwargs
        self.state = {k: None for k in kwargs}

    def check_updates(self, msg):
        needs_update = False
        for k, v in self.parts.items():
            new_value = v()
            old_value = self.state[k]
            if new_value != old_value:
                needs_update = True
                setattr(msg, k, new_value)
                msg.update = True

            self.state[k] = new_value
        return needs_update


class RobotState(object):
    def __init__(self, controller):
        self.controller = controller

        self.headlights = Component(on=controller.get_y)
        self.motor_right = Component(
            speed=self.calculate_motor_speed,
            breaks=controller.get_b)
        self.motor_left = Component(
            speed=lambda: int(controller.get_left_x() * 100),
            breaks=controller.get_b)

    def _neg(self, num):
        if num < 0:
            return -1
        return 1

    def calculate_motor_speed(self):
        x = self.controller.get_left_x()
        y = self.controller.get_left_y()

        forward_value = abs(int((abs(y) - abs(x)) * 100))

        if abs(x) > abs(y) or y > 0:
            if x > 0:
                forward_value *= -1
        #     100 + forward_value

        return int(x)

async def run(url):
    logger.info('Connecting to {}'.format(url))

    Controller.init()
    controller = Controller(0)

    robot_state = RobotState(controller)

    async with websockets.connect(url) as websocket:
        while True:
            controller.update()

            robot_msg = RobotMessage()

            # robot_msg.motor_left_rpm.update = True
            # robot_msg.motor_left_rpm.speed = 120
            #
            # robot_msg.motor_right_rpm.update = True
            # robot_msg.motor_right_rpm.speed = 120
            # robot_msg.arm.update = True
            # robot_msg.arm.degree = 70
            # robot_msg.wrist.update = True
            # robot_msg.wrist.degree = 2
            # robot_msg.camera.update = True
            # robot_msg.camera.degree = 2
            robot_msg.claw.update = True
            robot_msg.claw.degree = 200

            robot_state.headlights.check_updates(robot_msg.headlights)
            robot_state.motor_right.check_updates(robot_msg.motor_right)
            robot_state.motor_left.check_updates(robot_msg.motor_left)

            ser_msg = robot_msg.SerializeToString()

            await websocket.send(ser_msg)

            with suppress(asyncio.TimeoutError):
                msg = await asyncio.wait_for(websocket.recv(), .1)
                print(msg)


def main():
    config = get_config()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run("ws://{0.addr}:{0.port}".format(config)))
