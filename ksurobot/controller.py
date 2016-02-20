import asyncio
from .protocol.proto.main_pb2 import Robot as RobotMsg, BaseStation as BaseStationMsg


class Controller(object):
    def __init__(self, loop, robot, server):
        self.robot = robot
        self.server = server
        self.loop = loop

    def heart_beat(self):
        msg = BaseStationMsg()
        return msg.SerializeToString()

    def recv(self, msg_):
        msg = RobotMsg()
        msg.ParseFromString(msg_)

        if msg.headlights.update:
            robot.head_lights.set(msg.headlights.on)

        for motor_str in ('right', 'left'):
            motor = getattr(robot, 'motor_'+motor_str)
            msg = getattr(msg, 'motor_'+motor_str)
            if msg.update:
                if msg.breaks:
                    motor.set_brake(True)
                else:
                    motor.set(msg.speed)

    async def _wait_recv(self):
        while True:
            msg = await self.server.recv()
            self.recv(msg)

    async def _wait_heartbeat(self):
        while True:
            asyncio.sleep(400)
            msg = self.heart_beat()
            await self.server.send(msg)

    async def run(self):
        await asyncio.wait([
                self._wait_recv(),
                self._wait_heartbeat()
            ])
