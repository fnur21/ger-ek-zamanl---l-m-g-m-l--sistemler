import time
from machine import Pin

class HX711:
    def __init__(self, dout, pd_sck, gain=128):
        self.PD_SCK = Pin(pd_sck, Pin.OUT)
        self.DOUT = Pin(dout, Pin.IN)
        self.GAIN = 0

        self.OFFSET = 0
        self.SCALE = 1

        self.set_gain(gain)

    def is_ready(self):
        return self.DOUT.value() == 0

    def set_gain(self, gain):
        if gain == 128:
            self.GAIN = 1
        elif gain == 64:
            self.GAIN = 3
        elif gain == 32:
            self.GAIN = 2

        self.read()
    
    def read(self):
        while not self.is_ready():
            pass

        data = 0
        for _ in range(24):
            self.PD_SCK.value(1)
            data = data << 1 | self.DOUT.value()
            self.PD_SCK.value(0)

        for _ in range(self.GAIN):
            self.PD_SCK.value(1)
            self.PD_SCK.value(0)

        if data & 0x800000:
            data |= ~0xffffff

        return data

    def read_average(self, times=10):
        sum = 0
        for _ in range(times):
            sum += self.read()
        return sum // times

    def tare(self):
        self.OFFSET = self.read_average()

    def get_value(self, times=10):
        return self.read_average(times) - self.OFFSET

    def get_weight(self, times=10):
        return self.get_value(times) / self.SCALE

    def set_scale(self, scale):
        self.SCALE = scale
