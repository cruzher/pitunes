#!/usr/bin/python

import string
from subprocess import Popen, PIPE
import thread
import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime
import time
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
from Adafruit_I2C import Adafruit_I2C
import gaugette.rotary_encoder
import gaugette.switch

#LCD
lcd = Adafruit_CharLCDPlate()
lcd.begin(20, 4)
lcd.clear()

#Volume control
i2c = Adafruit_I2C(0x2A, 1, True)
i2c.write8(0x10, 0)
volume_max = 30
volume_visual_max = 8


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
current_datetime = ""
current_source = "Spotify"
current_playlist = ["nothing"]
current_playlist_pos = ""
current_radiostation = ""
current_playstatus = ""	#play, stop, pause
current_volume = 0

#Global Menu
menu_fristdraw = True
menu_active = False
menu_purpose = ""		#track or playlist
menu_pointer = None
menu_selected = None
menu_timeout = 0
menu_items = ["row1", "row2", "row3", "row4"]

#Global LCD
lcd_song = ""
lcd_datetime = ""
lcd_source = ""
lcd_playlist_length = 0
lcd_playlist_pos = 0
lcd_radiostation = "N/A"
lcd_redraw = False
lcd_playstatus = ""
## END VARIABLES

#GPIO
cheapamp_pin = 27
lcdbacklight_pin = 22
GPIO.setmode(GPIO.BCM)
GPIO.setup(cheapamp_pin, GPIO.OUT) #Cheapamp
GPIO.setup(lcdbacklight_pin, GPIO.OUT) #LCD Backlight
# Initial start of amp and backlight
GPIO.output(cheapamp_pin, True)
sleep(1)
GPIO.output(lcdbacklight_pin, True)

def navigate(direction):
	global menu_selected
	global menu_pointer
	global menu_lcd_start

	if (direction == "up"):
		if (menu_selected > 0):
			menu_selected -= 1
			if (menu_pointer > 1):
				menu_pointer -= 1
			else:
				menu_lcd_start -= 1
	else:
		if (menu_selected < len(menu_items) -1):
			menu_selected += 1
			if (menu_pointer < 3):
				menu_pointer +=1
			else:
				menu_lcd_start +=1

def checkinputs(): #Will be used as a thread
	global current_source
	global menu_active
	global menu_purpose
	global menu_timeout
	global current_playstatus
	global current_volume
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
				#Update timeout to keep menu active.
				menu_timeout = current_time + 10
				if (enc_left_delta<0): #rotating left
					navigate("up")
				elif (enc_left_delta>0): #rotating right
					navigate("down")
			elif (menu_active == False):
				menu_purpose = "track"
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
						menu_purpose = "playlist"
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
					if (current_volume < volume_max):
						#increase volume
						current_volume += 1
						print "Increasing Volume"
						i2c.write8(0x10, current_volume)
				elif (enc_right_delta>0): #rotating right
					if (current_volume > 0):
						#decrease volume
						current_volume -= 1
						print "Decreasing Volume"
						i2c.write8(0x10, current_volume)
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

def mopidyread():
	global current_song

	while (True):
		if (current_source == "Spotify"):
			current_song = Popen("mpc current -f \"%artist% - %title%\"", shell=True, stdout=PIPE).stdout.read()
	
		sleep(1)

def clearscreen():
	global lcd_radiostation
	global lcd_source
	global lcd_datetime
	global lcd_song
	global lcd_playlist_pos
	global lcd_playlist_length

	#reset lcd variables
	lcd_radiostation = None
	lcd_source = None
	lcd_datetime = None
	lcd_song = None
	lcd_playlist_pos = None
	lcd_playlist_length = None

	#clear LCD
	lcd.clear()

#Staring Threads
thread.start_new_thread(checkinputs, ())
thread.start_new_thread(mopidyread, ())

lcd.setCursor(9,3)
lcd.message("Vol"+chr(255)+chr(255)+chr(219)+chr(219)+chr(219)+chr(219)+chr(219)+chr(219))

while True:
	current_datetime = datetime.now().strftime("%Y-%m-%d     %H:%M")
	current_time = round(time.time())

	#Show message on screen when System is shutting down.
	try:
		with open('halting'):
			Popen("rm -f halting", shell=True)
			lcd.clear()
			lcd.setCursor(0,0)
			lcd.message("+------------------+")
			lcd.setCursor(0,1)
			lcd.message("|      SYSTEM      |")
			lcd.setCursor(0,2)
			lcd.message("|   SHUTTING DOWN  |")
			lcd.setCursor(0,3)
			lcd.message("+------------------+")
			break
	except IOError:
		sleep(0)


	#if menu is active
	if (menu_active == True): 
		if (menu_fristdraw == True):
			menu_timeout = current_time + 10
			menu_fristdraw = False
			clearscreen()
			if (menu_purpose == "track"):
				lcd.setCursor(7,0)
				lcd.message("Tracks")
			else:
				lcd.setCursor(5,0)
				lcd.message("Playlists")
			print "menu is active"
			
		#MENU STUFF

		#Close menu on timeout
		if (current_time > menu_timeout):
			print "deactivating menu"
			lcd_redraw = True
			menu_active = False
			menu_pointer = None
			menu_fristdraw = True
			menu_selected = None

	#if menu is not active
	else: 
		
		if (lcd_redraw == True):
			lcd_redraw = False
			clearscreen() 

		if (current_source == "Spotify"):
			
			#Update Time
			if (current_datetime != lcd_datetime):
				lcd.setCursor(0,0)
				lcd.message(current_datetime)
				lcd_datetime = current_datetime
				print "time: "+current_datetime

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