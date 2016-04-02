from time import time
from .bases import AbstractPart


class BaseEncoder(AbstractPart):
    def __init__(self, ticks_per_rev=1200):
        self.ticks_per_rev = ticks_per_rev
        self.past_ticks = 0
        self.past_time = time()

    def get_ticks(self):
        raise NotImplemented

    def get_update_delta(self):
        ticks, new_time = self.get_ticks(), time()
        past_ticks, past_time = self.past_ticks, self.past_time
        self.past_ticks = ticks
        self.past_time = new_time
        return ticks - past_ticks, new_time - past_time

    def get(self):
        """Return speed as rpm"""
        dticks, dtime = self.get_update_delta()

        return (60 / dtime) * (dticks / self.ticks_per_rev)
