import RPi.GPIO as GPIO
from time import sleep

while True:
	print GPIO.input(12);
	sleep(.5)