#!/usr/bin/python

import string
import subprocess
import thread
from time import sleep
from datetime import datetime
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import gaugette.rotary_encoder
import gaugette.switch

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
mopidy_playlist_length = 
mopidy_playlist_position = 
mopidy_playlist = ["first song", "next song", "next song again"]
menu_position
menu_lcd_start

def checkinputs():
	while True:
		if (interface_state = 2 and interface_change_track == False):
			#RIGHT ENCODER
			if (enc_right_delta != 0 and enc_right_seq == 2):
				#Starting to move means to switch track
				interface_change_track = True
		
		if (interface_change_track == True):
			
				
thread.start_new_thread(checkinputs, ())


#Main Thread
while True:
	#menu
	
