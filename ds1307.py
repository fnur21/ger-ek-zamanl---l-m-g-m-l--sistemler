from machine import I2C
import time

class DS1307:
    def __init__(self, i2c):
        self.i2c = i2c
        self.addr = 0x68

    def bcd2dec(self, bcd):
        return (bcd >> 4) * 10 + (bcd & 0x0F)

    def dec2bcd(self, dec):
        return ((dec // 10) << 4) | (dec % 10)

    def get_time(self):
        try:
            data = self.i2c.readfrom_mem(self.addr, 0x00, 3)
            second = self.bcd2dec(data[0] & 0x7F)  # saniyede CH biti var
            minute = self.bcd2dec(data[1])
            hour = self.bcd2dec(data[2])
            return "{:02d}:{:02d}:{:02d}".format(hour, minute, second)
        except:
            return "RTC HATASI!"

    def get_date(self):
        try:
            data = self.i2c.readfrom_mem(self.addr, 0x04, 3)
            day = self.bcd2dec(data[0])
            month = self.bcd2dec(data[1])
            year = self.bcd2dec(data[2]) + 2000
            return "{:04d}-{:02d}-{:02d}".format(year, month, day)
        except:
            return "Tarih okunamıyor"

    def set_time(self, hour, minute, second):
        data = bytearray(3)
        data[0] = self.dec2bcd(second)
        data[1] = self.dec2bcd(minute)
        data[2] = self.dec2bcd(hour)
        self.i2c.writeto_mem(self.addr, 0x00, data)

    def set_date(self, day, month, year):  # örn: 27, 5, 2025
        data = bytearray(3)
        data[0] = self.dec2bcd(day)
        data[1] = self.dec2bcd(month)
        data[2] = self.dec2bcd(year % 100)
        self.i2c.writeto_mem(self.addr, 0x04, data)
