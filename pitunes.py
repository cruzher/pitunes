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
volume_max = 60
volume_visual_max = 18
volume_default = 5
i2c = Adafruit_I2C(0x2A, 1, False)
i2c.write8(0x10, volume_default) #Default Volumelevel



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
spotify_active = True
connected_to_network = False
connected_to_spotify = False
mopidy_is_running = False
current_artist = ""
current_song = ""
current_time = ""
current_datetime = ""
current_source = "Spotify"
current_playlist = ["nothing"]
current_playlist_pos = ""
current_radiostation = ""
current_playstatus = False	#play, stop, pause
current_volume = volume_default

#Global Menu
menu_fristdraw = True
menu_active = False
menu_purpose = ""		#track or playlist
menu_pointer = 1
menu_selected = 0
menu_timeout = 0
menu_items = ["row1", "row2", "row3", "row4"]
menu_start = 0

#Global LCD
lcd_song = ""
lcd_datetime = ""
lcd_source = ""
lcd_playlist_length = 0
lcd_playlist_pos = 0
lcd_radiostation = "N/A"
lcd_redraw = False
lcd_playstatus = ""
lcd_volume = None
lcd_menu_pointer = -1
lcd_menu_start = -1
lcd_scroll_counter = 0
lcd_scroll_pos = 0
lcd_scroll_str = ""
## END VARIABLES

#GPIO
cheapamp_pin = 27
lcdbacklight_pin = 22
atxraspi_pin_in = 24
atxraspi_pin_out = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(atxraspi_pin_out, GPIO.OUT)
GPIO.setup(atxraspi_pin_in, GPIO.IN)
GPIO.setup(cheapamp_pin, GPIO.OUT) #Cheapamp
GPIO.setup(lcdbacklight_pin, GPIO.OUT) #LCD Backlight
# Telling atxraspi boot-finished
GPIO.output(atxraspi_pin_out, True)
# Power ON Amp
GPIO.output(cheapamp_pin, True)
sleep(1)
# Power ON LCD Backlight
GPIO.output(lcdbacklight_pin, True)

def navigate(direction):
	global menu_selected
	global menu_pointer
	global menu_start

	if (direction == "up"):
		if (menu_selected > 0):
			menu_selected -= 1
			if (menu_pointer > 1):
				menu_pointer -= 1
			elif (menu_start > 0):
				menu_start -= 1
	else:
		if (menu_selected < len(menu_items) -1):
			menu_selected += 1
			if (menu_pointer < 3):
				menu_pointer +=1
			elif (menu_start < len(menu_items) -3):
				menu_start +=1

def checkinputs(): #Will be used as a thread
	global current_source
	global menu_active
	global menu_items
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

				if (enc_left_delta>0): #rotating left
					navigate("up")

				elif (enc_left_delta<0): #rotating right
					navigate("down")

			elif (menu_active == False):
				menu_purpose = "track"
				menu_items = current_playlist
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
					if (menu_purpose == "track"):
						Popen("mpc play "+str(menu_selected+1), shell=True, stdout=PIPE).stdout.read()
						print menu_items[menu_selected]
					if (menu_purpose == "playlist"):
						Popen("mpc clear", shell=True, stdout=PIPE).stdout.read()
						Popen("mpc load \"" + menu_items[menu_selected] + "\"", shell=True, stdout=PIPE).stdout.read()
						Popen("mpc play 1", shell=True, stdout=PIPE).stdout.read()
						print "Loading playlist: " + menu_items[menu_selected]
					closeMenu()
				else:
					if (current_source == "Spotify"):
						#activate menu (change playlist)
						menu_purpose = "playlist"
						playlists = Popen("php5 playlist.php -spotify", shell=True, stdout=PIPE).stdout.read()
						menu_items = playlists.split('\n')
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
						i2c.write8(0x10, current_volume)
				elif (enc_right_delta>0): #rotating right
					if (current_volume > 0):
						#decrease volume
						current_volume -= 1
						i2c.write8(0x10, current_volume)
		## END Right encoder rotating ##


		## Right switch pressed ##
		if (sw_right_state == 1):
			if (right_count < 50):
				right_count += 1
			elif(right_held == False): #Button is held down
				right_held = True
				if (menu_active == False):
					## Open generall menu.
					print "mekk"
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
	global current_playlist
	global mopidy_is_running
	global connected_to_spotify

	while (True):
		if (current_source == "Spotify"):
			if (connected_to_spotify == True):
				current_song = Popen("mpc current -f \"%artist% - %title%\"", shell=True, stdout=PIPE).stdout.read()

				#playlist
				playlist = Popen("mpc playlist -f \"%title% - %artist%\"", shell=True, stdout=PIPE).stdout.read()
				playlist = str(playlist)
				playlist = playlist[:-10]
				current_playlist = playlist.split('\n')

		if (connected_to_spotify == False):
			spotify_check = Popen("mpc lsplaylists", shell=True, stdout=PIPE, stderr=PIPE).stdout.read()
			if (spotify_check != ""):
				print "Connected to spotify"
				connected_to_spotify = True
		sleep(1)

def clearscreen():
	global lcd_radiostation
	global lcd_source
	global lcd_datetime
	global lcd_song
	global lcd_playlist_pos
	global lcd_playlist_length
	global lcd_menu_start
	global lcd_menu_pointer

	#reset lcd variables
	lcd_radiostation = None
	lcd_source = None
	lcd_datetime = None
	lcd_song = None
	lcd_playlist_pos = None
	lcd_playlist_length = None
	lcd_volume = None
	lcd_menu_pointer = -1
	lcd_menu_start = -1

	#clear LCD
	lcd.clear()

def closeMenu():
	global menu_active
	global menu_pointer
	global menu_fristdraw
	global menu_selected
	global menu_start
	global lcd_redraw
	print "deactivating menu"
	lcd_redraw = True
	menu_active = False
	menu_pointer = 1
	menu_fristdraw = True
	menu_selected = 0
	menu_start = 0


#INIT
lcd.clear()
lcd.setCursor(4,0)
lcd.message("STARTING UP.")
lcd.setCursor(0,1)
lcd.message("Network         [  ]")
lcd.setCursor(0,2)
lcd.message("Mopidy          [  ]")
if (spotify_active == True):
	lcd.setCursor(0,3)
	lcd.message("Spotify         [  ]")

while (mopidy_is_running == False):
	mopidy_check = Popen("mpc", shell=True, stdout=PIPE, stderr=PIPE).stdout.read()
	if (mopidy_check != ""):
		lcd.setCursor(17,2)
		lcd.message("OK")
		mopidy_is_running = True
	sleep(1)

if (spotify_active == True):
	while (connected_to_spotify == False):
		spotify_check = Popen("mpc lsplaylists", shell=True, stdout=PIPE, stderr=PIPE).stdout.read()
		if (spotify_check != ""):
			lcd.setCursor(17,3)
			lcd.message("OK")
			connected_to_spotify = True
	sleep(1)

lcd.clear()

#Staring Threads
thread.start_new_thread(checkinputs, ())
thread.start_new_thread(mopidyread, ())

#INIT END

while True:
	current_datetime = datetime.now().strftime("%Y-%m-%d     %H:%M")
	current_time = round(time.time())

	#Show message on screen when System is shutting down.
	if (GPIO.input(atxraspi_pin_in)):
		lcd.clear()
		#lcd.setCursor(0,0)
		#lcd.message("+------------------+")
		lcd.setCursor(0,1)
		lcd.message("       SYSTEM")
		lcd.setCursor(0,2)
		lcd.message("    SHUTTING DOWN")
		#lcd.setCursor(0,3)
		#lcd.message("+------------------+")
		i2c.write8(0x10, 0)
		GPIO.output(cheapamp_pin, False) #Turn off Amp
		Popen("sudo halt", shell=True)
		break


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
		############	
		#MENU STUFF#
		############

		#MenuPointer
		if (menu_pointer != lcd_menu_pointer):
			lcd.setCursor(0,1)
			lcd.message("  ")
			lcd.setCursor(0,2)
			lcd.message("  ")
			lcd.setCursor(0,3)
			lcd.message("  ")
			lcd.setCursor(0,menu_pointer)
			lcd.message("> ")
			lcd_menu_pointer = menu_pointer

		if (menu_start != lcd_menu_start):
			for i in range(0,3):
				lcd.setCursor(2,i+1)
				lcd.message("                  ")
				lcd.setCursor(2, i+1)
				lcd.message(menu_items[menu_start + i][:18])
			lcd_menu_start = menu_start

		###################
		# MENU STUFF ENDS #
		################### 

		#Close menu on timeout
		if (current_time > menu_timeout):
			closeMenu()

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

			#Print Source
			if (current_source != lcd_source):
				lcd.setCursor(0,1)
				lcd.message(current_source)
				lcd_source = current_source

			#Update Song
			if (current_song != lcd_song):
				lcd.setCursor(0,2)
				lcd.message("                    ")
				lcd.setCursor(0,2)
				lcd.message(current_song[:20])
				lcd_song = current_song

			#Scroll Song if longer then 20.
			if (len(lcd_song) > 20):
				lcd_scroll_str = lcd_song+" "+lcd_song
				if (lcd_scroll_counter >= 15):
					start = lcd_scroll_pos + 1
					end = start + 20
					lcd.setCursor(0,2)
					lcd.message(lcd_scroll_str[start:end])
					if (start >= len(lcd_song)):
						lcd_scroll_pos = 0
					else:
						lcd_scroll_pos += 1
					lcd_scroll_counter = 0
				else:
					lcd_scroll_counter += 1

			#Update Volume
			if (current_volume != lcd_volume):
				lcd.setCursor(0,3)
				volume_visual = round(current_volume / (volume_max / volume_visual_max))
				volume_rest = volume_visual_max - volume_visual 
				vol_print = "-"
				for i in range(1,19):
					if (i <= volume_visual):
						vol_print = vol_print + chr(255)
					else:
						vol_print = vol_print + chr(219)
				lcd.message(vol_print+"+")

		if (current_source == "Radio"):
			print "Source is Radio"
	sleep(.01)