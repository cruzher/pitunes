#!/usr/bin/python

from Adafruit_I2C import Adafruit_I2C
from time import sleep

addr = 0x2A
bus = Adafruit_I2C(addr, 1, True)

bus.readU16(0x00, 3)