import spidev


class DistanceSensor(object):
    def __init__(self, channel):
        self.channel = channel
        self.spi = None

    def __enter__(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0,0)
        return self

    def __exit__(self, *enc):
        self.spi = None

    def get(self):
        data = self.spi.xfer2([1,(8+self.channel)<<4,0])
        return data
