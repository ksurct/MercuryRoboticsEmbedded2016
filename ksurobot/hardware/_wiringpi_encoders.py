from pathlib import Path
from ctypes import POINTER, c_long, c_char, c_int

from .utils import Wrapper

wiring_interupts = Wrapper(str(Path(__file__).parent/'_wiring_encoders.so'))


@wiring_interupts.wrap([POINTER(c_long), c_int, c_int], None)
def setup_speed_pin(last_tick, pin_a, pin_b):
    pass
