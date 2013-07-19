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

#Global Variables
last_timeNow = None
last_mopidy_track = None
last_source = None
last_interface_state = None
volume_current = 10
airplay_lock = False
interface_state = 2		# 0=Idle 1=Radio 2=Spotify 3=AirPlay
interface_change_track = False	# Will Override interface to show menu
idle_start = None		
mopidy_playing = False

def changestate(state):
	interface_state = state
	
	#Make sure the LCD will redraw
	lcd.clear()
	last_source = None
	last_mopidy_track = None
	last_timeNow = None
	
	
	if (interface_state == 1):
		#Clear current playlist
		subprocess.Popen("mpc clear", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		##Load Radio Playlist
		##Play first Station
		#subprocess.Popen("mpc play 1", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
	if (interface_state == 2):
		#Clear current playlist
		subprocess.Popen("mpc clear", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	

def changevolume():
	global volume_current
	volume_last = 0
	
	while True:
		if (volume_last != volume_current):
			print volume_current
			volume_last = volume_current
		sleep(.01)

def checkinput():
	global volume_current
	global mopidy_playing
	global interface_state
	enc_left_state_last = enc_left.rotation_state()
	right_count = 0
	left_count = 0
	
	while True:
		enc_right_delta = enc_right.get_delta()
		enc_right_seq = enc_right.rotation_sequence()
		enc_left_delta = enc_left.get_delta()
		enc_left_seq = enc_left.rotation_sequence()
		sw_right_state = sw_right.get_state()
		sw_left_state = sw_left.get_state()


		##
		##INTERNET RADIO
		##
		if (interface_state == 1 and interface_change_track == False):
			echo "mekk"
		##
		## SPOTIFY
		##
		if (interface_state == 2 and interface_change_track == False):
			#RIGHT SWITCH
			if (sw_right_state == 1):
				if (right_count < 50):
					right_count += 1
				elif (right_count < 100): #Button held down
					right_count = 101 #So value is just registerd once
					subprocess.Popen("mpc stop", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
					mopidy_playing = False	
			else:
				if (right_count >0 and right_count < 50): #Button pressed
					if(mopidy_playing == True):
						subprocess.Popen("mpc pause", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
						mopidy_playing = False
					else:
						subprocess.Popen("mpc play", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
						mopidy_playing = True
	
				right_count = 0 #Resetting Counter for next press.
	
	
			#RIGHT ENCODER
			if (enc_right_delta != 0 and enc_right_seq == 2):
				if (enc_right_delta<0 and volume_current <= 95):
					volume_current += 5
				elif (enc_right_delta>0 and volume_current >= 5):
					volume_current -= 5
	
	
			#LEFT SWITCH
			if (sw_left_state == 1):
				if (left_count < 50):
					left_count += 1
					
				elif (left_count < 100): 
					left_count = 101
					# Do this if button is held down
					changestate(1) #Byter till Radio
						
			else:
				if (left_count >0 and left_count < 50): 
					#Do this if button is pressed once
					interface_change_track = True
					print "Byter Spellista"
					
				#Reset hold-counter
				left_count = 0 
			
			
			#LEFT ENCODER
			if (enc_left_delta != 0 and enc_left_seq == 2):
				if (enc_left_delta<0):
					#One step right
					subprocess.Popen("mpc next", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				elif (enc_left_delta>0):
					#One step left
					subprocess.Popen("mpc prev", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		## SPOTIFY END ##
		
		##
		## AIRPLAY
		##
		if (interface_state == 3 and interface_change_track == False):
			#RIGHT ENCODER
			if (enc_right_delta != 0 and enc_right_seq == 2):
				if (enc_right_delta<0 and volume_current <= 95):
					volume_current += 5
				elif (enc_right_delta>0 and volume_current >= 5):
					volume_current -= 5
		## AIRPLAY END ##
		
		
		##
		## MENU TO CHANGE TRACK/STATION
		##
		if (interface_change_track == True):
			## WOOP WOOP
		
		sleep(.01) 
		## ENF OF LOOP ##

#Staring Threads
thread.start_new_thread(checkinput, ())
thread.start_new_thread(changevolume, ())

while True:
	timeNow = datetime.now().strftime("%Y-%m-%d %H:%M")
	
	pArtist = subprocess.Popen("mpc current -f \"%artist% - %title%\"", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	mopidy_track, errSong = pArtist.communicate()
	pTrack = subprocess.Popen("mpc |grep \"#\"", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	track_info, errSong = pTrack.communicate()
	pairplay = subprocess.Popen("netstat -t |grep rfe", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	airplay, errAirplay = pairplay.communicate()
	

	if (airplay and airplay_lock == False):
		last_timeNow = None
		lcd.clear()
		lcd.setCursor(6,2)
		lcd.message("Airplay")
		airplay_lock = True
		last_interface_state = interface_state
		interface_state = 3
	elif (not airplay and airplay_lock == True):
		last_mopidy_track = None
		airplay_lock = False
		interface_state = last_interface_state

	#LCD Update Time
	if (timeNow != last_timeNow):
		lcd.setCursor(0,0)
		lcd.message(timeNow)
		last_timeNow = timeNow
		print "time: "+timeNow
		
	if (interface_state == 1):
		lcd_source = "Radio"
	elif (interface_state == 2):
		lcd_source = "Spotify     "
	if (last_source != lcd_source):
		last_source = lcd_source
		lcd.setCursor(0,1)
		lcd.message("                    ")
		lcd.setCursor(0,1)
		lcd.message(lcd_source)
		print "Source: "+lcd_source
	
	if (mopidy_track != last_mopidy_track):
		lcd.setCursor(0,2)
		lcd.message("                    ")
		lcd.setCursor(0,2)
		lcd.message(mopidy_track[:-1][:20])
		last_mopidy_track = mopidy_track
		print "Song: "+mopidy_track[:-1]
	
	sleep(0.01)
