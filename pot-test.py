#!/usr/bin/python

import smbus
from time import sleep

bus = smbus.SMBus(1)
addr = 0x2A

def read():
	wiper = bus.read_byte_data(addr, 3)
	return wiper

def write(value):
	bus.write_byte_data(addr, -1, value)

while True:
	print read()

	sleep(1)