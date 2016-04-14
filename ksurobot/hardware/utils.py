from ctypes import cdll
from ..util import get_config


class Wrapper(object):
    def __init__(self, library):
        self.library_name = library
        self.library = None

    def load(self):
        if self.library is None:
            config = get_config()
            if config.emulate:
                self.library = False
            else:
                self.library = cdll.LoadLibrary(self.library_name)

        return self.library

    def wrap(self, args, result):
        lib = self.load()
        def _w(func):
            if lib:
                func = getattr(lib, func.__name__)
                func.argtypes = args
                func.restype = result
            return func
        return _w
