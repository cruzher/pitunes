#!/usr/bin/python

import smbus
from time import sleep

bus = smbus.SMBus(1)
addr = Ax2A

def read():
	wiper = bus.read_byte_data(address, 3)
	return wiper

def write(value):
	bus.write_byte_data(address, -1, value)

while True:
	print read()

	sleep(1)