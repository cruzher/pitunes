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
GPIO.output(27, True)
GPIO.output(22, True)

#LCD
lcd = Adafruit_CharLCDPlate()
lcd.begin(20, 4)
lcd.clear()

#Rotary Encoders
enc_left_pin_a = 14
enc_left_pin_b = 13
sw_left_pin = 12
enc_left = gaugette.rotary_encoder.RotaryEncoder(enc_left_pin_a, enc_left_pin_b)
sw_left = gaugette.switch.Switch(sw_left_pin)


#global variables
interface_state = 2
interface_change_track = False
interface_change_playlist = False
mopidy_playlist_position = 5
mopidy_playlist = ["Row 1", "Row 2"]
menu_active = False
menu_position = 0
menu_lcd_position = 1
menu_lcd_position_last = None
menu_lcd_start = 0
menu_lcd_start_last = None
menu_timeout = 0

def timeout():
	global interface_change_track
	global menu_timeout
	global menu_lcd_start_last
	
	while True:
		if (interface_change_track == True):
			menu_timeout += 1
			if (menu_timeout > 10):
				interface_change_track = False
				clearscreen()
				menu_timeout = 0
				
		sleep(1)

def checkinputs():
	global interface_change_track
	global menu_lcd_start
	global menu_lcd_position
	global menu_position
	global menu_timeout
	global mopidy_playlist
	global mopidy_playlist_position
	left_count = 0
	
	while True:
		enc_left_delta = enc_left.get_delta()
		enc_left_seq = enc_left.rotation_sequence()
		sw_left_state = sw_left.get_state()
		
		if (interface_state == 2 and interface_change_track == False):
			#LEFT ENCODER
			if (enc_left_delta != 0 and enc_left_seq == 2):
				#Starting to move means to switch track
				interface_change_track = True
		
		if (interface_change_track == True):
			#LEFT ENCODER
			if (enc_left_delta != 0 and enc_left_seq == 2):
				menu_timeout = 0
				if (enc_left_delta<0):
					if (menu_lcd_position < 4):
						menu_lcd_position +=1
					elif (menu_lcd_start < len(mopidy_playlist) - 4):
						menu_lcd_start += 1
					if (menu_position < len(mopidy_playlist) -1):
						menu_position += 1
				elif (enc_left_delta>0):
					if (menu_lcd_position > 1):
						menu_lcd_position -= 1
					elif (menu_lcd_start > 0):
						menu_lcd_start -= 1
					if (menu_position > 0):
						menu_position -= 1
						
			#LEFT SWITCH
			if (sw_left_state == 1):
				if (left_count < 50):
					left_count += 1
			else:
				if (left_count >0 and left_count < 50): 
					#Do this if button is pressed once
					song_to_play = str(menu_position + 1)
					interface_change_track = False
					lcd.clear()
					subprocess.Popen("mpc -q play "+song_to_play, shell=True, stdout=subprocess.PIPE)
					
				#Reset hold-counter
				left_count = 0 
		sleep(.01)
				
thread.start_new_thread(checkinputs, ())
thread.start_new_thread(timeout, ())

def clearscreen():
	global menu_lcd_start_last
	global menu_lcd_position_last
	
	
	menu_lcd_start_last = None
	menu_lcd_position_last = None
	sleep(.1)
	lcd.clear()

#Main Thread
while True:
	#menu
	if (interface_change_track == True):
		playlist = subprocess.Popen("mpc playlist -f \"%title% - %artist%\"", shell=True, stdout=subprocess.PIPE)
		mopidy_playlist_position = subprocess.Popen("mpc current -f %position%", shell=True, stdout=subprocess.PIPE)
		playlist = playlist.communicate()
		playlist = str(playlist)
		playlist = playlist[2:-10]
		mopidy_playlist = playlist.split('\\n')
		mopidy_playlist_position = mopidy_playlist_position.communicate()
		mopidy_playlist_position = str(mopidy_playlist_position)
		mopidy_playlist_position = mopidy_playlist_position[2:-10]
		
		if (menu_lcd_start_last != menu_lcd_start):
			menu_lcd_start_last = menu_lcd_start
			lcd.clear()
			for x in range(0,4):
				lcd.setCursor(2, x)
				lcd.message(mopidy_playlist[menu_lcd_start + x][:18])
		if (menu_lcd_position_last != menu_lcd_position):
			lcd.setCursor(0,0)
			lcd.message(" ")
			lcd.setCursor(0,1)
			lcd.message(" ")
			lcd.setCursor(0,2)
			lcd.message(" ")
			lcd.setCursor(0,3)
			lcd.message(" ")
			lcd.setCursor(0,menu_lcd_position -1)
			lcd.message(">")
			menu_lcd_position_last = menu_lcd_position

	sleep(.01)
