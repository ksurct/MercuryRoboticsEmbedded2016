from .controller import Controller
from ..protocol.proto.main_pb2 import Robot as RobotMessage
import asyncio
import websockets


class Robot(object):
    headlights = False


async def run():
    robot_state = Robot()

    Controller.init()
    controller = Controller(0)
    async with websockets.connect('ws://localhost:5678') as websocket:
        while True:
            controller.update()

            robot_msg = RobotMessage()

            if robot_state.headlights != controller.get_y():
                robot_state.headlights = controller.get_y()
                robot_msg.headlights.update = True
                robot_msg.headlights.on = False

            ser_msg = robot_msg.SerializeToString()

            await websocket.send(ser_msg)
            await asyncio.sleep(.1)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


# async def tick():
#     await hello()
#
#     await asyncio.sleep(1.1)
#     asyncio.ensure_future(tick())
#
#
# def main():
#     asyncio.ensure_future(tick())
#     asyncio.get_event_loop().run_forever()
