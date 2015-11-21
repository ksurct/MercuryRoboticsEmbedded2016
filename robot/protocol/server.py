import asyncio

from .proto import main_pb2


class Server(object):
    def __init__(self, port, loop=None):
        self.port = port
        self.loop = asyncio.get_event_loop() if loop is None else loop

    def __enter__(self):
        return self

    def __exit__(self, *enc):
        pass

    def parse_message(self, msg):
        return main_pb2.Robot.ParseFromString(msg)

    def serialize_message(self, msg):
        return main_pb2.BaseStation.SerializeToString()
