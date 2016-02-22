from .controller import Controller
from ..protocol.proto.main_pb2 import Robot as RobotMessage
from ..util import get_config
import asyncio
import websockets
import logging

logger = logging.getLogger(__name__)


class Robot(object):
    headlights = False


async def run(url):
    logger.info('Connecting to {}'.format(url))
    robot_state = Robot()

    Controller.init()
    controller = Controller(0)
    async with websockets.connect(url) as websocket:
        while True:
            controller.update()

            robot_msg = RobotMessage()

            if robot_state.headlights != controller.get_y():
                robot_state.headlights = controller.get_y()
                robot_msg.headlights.update = True
                robot_msg.headlights.on = robot_state.headlights

            ser_msg = robot_msg.SerializeToString()

            await websocket.send(ser_msg)
            await asyncio.sleep(.1)


def main():
    config = get_config()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run("ws://{0.addr}:{0.port}".format(config)))
