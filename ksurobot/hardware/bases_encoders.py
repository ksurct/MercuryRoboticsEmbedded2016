from time import time
from .bases import AbstractPart


class BaseEncoder(AbstractPart):
    def __init__(self, ticks_per_rev=1200, reverse=False):
        self.ticks_per_rev = ticks_per_rev
        self.past_ticks = 0
        self.past_time = time()
        self._value = 0
        self._reverse = reverse

    def get_ticks(self):
        raise NotImplemented

    def get_update_delta(self):
        ticks, new_time = self.get_ticks(), time()
        past_ticks, past_time = self.past_ticks, self.past_time
        self.past_ticks = ticks
        self.past_time = new_time
        return ticks - past_ticks, new_time - past_time

    def update(self):
        dticks, dtime = self.get_update_delta()

        self._value = (60 / dtime) * (dticks / self.ticks_per_rev)
        if self._reverse:
            self._value = -self._value

    def get(self):
        """Return speed as rpm"""
        return self._value
