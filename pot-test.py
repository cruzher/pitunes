#!/usr/bin/python

from Adafruit_I2C import Adafruit_I2C
from time import sleep

addr = 0x2A
reg = 0x10
bus = Adafruit_I2C(addr, 1, True)

 bus.write8(reg, 3)
 sleep(10)
 bus.write8(reg, 0)