#!/usr/bin/python

import string
from subprocess import Popen, PIPE
import thread
import RPi.GPIO as GPIO
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

##VARIABLES
#Global Main
current_song = ""
current_time = ""
current_source = "Spotify"
current_playlist = ["mekk", "mekking"]
current_playlist_pos = ""
current_radiostation = ""
current_playstatus = False

#Global Menu
menu_active = False
menu_purpose = ""		#track or source
menu_pointer = None
menu_selected = None
menu_timeout = 0

#Global LCD
lcd_song = ""
lcd_time = ""
lcd_source = ""
lcd_playlist_length = 0
lcd_playlist_pos = 0
lcd_radiostation = "N/A"
lcd_redraw = False
## END VARIABLES

#GPIO
cheapamp_pin = 27
lcdbacklight_pin = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(cheapamp_pin, GPIO.OUT) #Cheapamp
GPIO.setup(lcdbacklight_pin, GPIO.OUT) #LCD Backlight
# Initial start of amp and backlight
GPIO.output(cheapamp_pin, True)
GPIO.output(lcdbacklight_pin, True)

def timeouts(): #Will be used as a thread
	while True:
		print "hello" 
		#Close menu on timeout

		#Activate standby mode if nothing is playing for 5 minutes

def checkinputs(): #Will be used as a thread
	global current_source
	global menu_active
	global current_playstatus
	left_count = 0
	left_held = False
	right_count = 0
	right_held = False

	while True:
		enc_right_delta = enc_right.get_delta()
		enc_right_seq = enc_right.rotation_sequence()
		enc_left_delta = enc_left.get_delta()
		enc_left_seq = enc_left.rotation_sequence()
		sw_right_state = sw_right.get_state()
		sw_left_state = sw_left.get_state()

		## Left encoder rotating ##
		if (enc_left_delta != 0 and enc_left_seq == 2):
			if (menu_active == True): 
				if (enc_left_delta<0): #rotating left
					if (menu_selected > 0):
						menu_selected -= 1
				elif (enc_left_delta>0): #rotating right
					if (menu_selected < len(current_playlist)):
						menu_selected += 1
			elif (menu_active == False):
				if (current_source == "Spotify"): 
					menu_active = True
				if (current_source == "Radio"): 
					menu_active = True
		## END Left encoder rotating ##


		## left switch pressed ##
		if (sw_left_state == 1):
			if (left_count < 50):
				left_count += 1
		else:
			if (left_count >0 and left_count < 50): #button is pressed once
				if (menu_active == True):
					#choose selected item
					print "choosing selected item"
				if (menu_active == False):
					if (current_source == "Spotify"):
						#activate menu (change playlist)
						menu_active = True
					if (current_source == "Radio"):
						#Like this song (saves to logfile)
						print "I Like This Song"
			elif (left_count >0 and left_count > 50): #button is held down
				if (menu_active == False):
					if (current_source == "Spotify"):
						current_source == "Radio"
					if (current_source == "Radio"):
						current_source == "Spotify"

			##Reset hold-counter##
			left_count = 0
		## END left switch pressed ##


		## Right encoder rotating ##
		if (enc_right_delta != 0 and enc_right_seq == 2):
			if (menu_active == False): #if menu is not active
				if (enc_right_delta<0): #rotating left
					#increase volume
					print "Increasing Volume"
				elif (enc_right_delta>0): #rotating right
					#decrease volume
					print "Decreasing Volume"
		## END Right encoder rotating ##


		## Right switch pressed ##
		if (sw_right_state == 1):
			if (right_count < 50):
				right_count += 1
			elif(right_held == False): #Button is held down
				right_held = True
				if (menu_active == False):
					if (current_source == "Spotify"):
						Popen("mpc -q stop", shell=True)
						current_playstatus = False
		else:
			if (right_count >0 and right_count < 50): #button is pressed once
				if (menu_active == False):
					if (current_source == "Spotify"):
						if (current_playstatus == False):
							Popen("mpc -q play", shell=True)
							current_playstatus = True
						else:
							Popen("mpc -q pause", shell=True)
							current_playstatus = False
					if (current_source == "Radio"):
						if (current_playstatus == False):
							Popen("mpc -q play", shell=True)
							current_playstatus = True
						else:
							Popen("mpc -q stop", shell=True)
							current_playstatus = False

			##Reset hold-counter##
			right_count = 0
			right_held = False
		## Right switch pressed ##
		sleep(.01)


def clearscreen():
	#reset lcd variables
	lcd_radiostation = None
	lcd_source = None
	lcd_time = None
	lcd_song = None
	lcd_playlist_pos = None
	lcd_playlist_length = None

	#clear LCD
	lcd.clear()

#Staring Threads
thread.start_new_thread(checkinputs, ())

while True:
	#if menu is active
	if (menu_active == True): 
		print "menu is active"

	#if menu is not active
	else: 
		current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
		current_song = Popen("mpc current -f \"%artist% - %title%\"", shell=True, stdout=PIPE).stdout.read()
		
		if (lcd_redraw == True):
			clearscreen() 

		if (current_source == "Spotify"):
			
			#Update Time
			if (current_time != lcd_time):
				lcd.setCursor(0,0)
				lcd.message(current_time)
				lcd_time = current_time
				print "time: "+current_time

			#Print Source
			if (current_source != lcd_source):
				lcd.setCursor(0,1)
				lcd.message(current_source)
				lcd_source = current_source

			#Update Songposition
			if (current_playlist_pos != lcd_playlist_pos):
				lcd.setCursor(0,10)

			#Update Song
			if (current_song != lcd_song):
				lcd.setCursor(0,2)
				lcd.message(current_song[:20])
				lcd_song = current_song


		if (current_source == "Radio"):
			print "Source is Radio"
	sleep(.01)