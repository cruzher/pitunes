#!/usr/bin/python

import string
import subprocess
import thread
import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import gaugette.rotary_encoder
import gaugette.switch

#GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(27, GPIO.OUT) #Cheapamp
GPIO.setup(22, GPIO.OUT) #LCD Backlight

#LCD
lcd = Adafruit_CharLCDPlate()
lcd.begin(20, 4)
lcd.clear()

#Rotary Encoders
enc_right_pin_a = 11
enc_right_pin_b = 10
sw_right_pin = 6
enc_left_pin_a = 14
enc_left_pin_b = 13
sw_left_pin = 12
enc_right = gaugette.rotary_encoder.RotaryEncoder(enc_right_pin_a, enc_right_pin_b)
sw_right = gaugette.switch.Switch(sw_right_pin)
enc_left = gaugette.rotary_encoder.RotaryEncoder(enc_left_pin_a, enc_left_pin_b)
sw_left = gaugette.switch.Switch(sw_left_pin)


#global variables
interface_state = 2
interface_change_track = False
interface_change_playlist = False
mopidy_playlist_length = 70
mopidy_playlist_position = 5
mopidy_playlist = ["first song", "next song", "next song again", "and again", "ohh so many"]
menu_position = 1
menu_lcd_start = 0

def checkinputs():
	while True:
		enc_right_delta = enc_right.get_delta()
		enc_right_seq = enc_right.rotation_sequence()
		sw_right_state = sw_right.get_state()
		
		if (interface_state == 2 and interface_change_track == False):
			#RIGHT ENCODER
			if (enc_right_delta != 0 and enc_right_seq == 2):
				#Starting to move means to switch track
				interface_change_track = True
		
		if (interface_change_track == True):
			print "nothing"
				
thread.start_new_thread(checkinputs, ())


#Main Thread
while True:
	#menu
	if (interface_change_track == True):
		for x in range(0,3):
			print mopidy_playlist[menu_lcd_start + x]

	sleep(2)
