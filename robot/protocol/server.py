from .proto import main_pb2


class Server(object):
    def __init__(self, port):
        self.port = port

    def __enter__(self):
        return self

    def __exit__(self, *enc):
        pass
