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
enc_right_pin_a = 14
enc_right_pin_b = 13
sw_right_pin = 12
enc_left_pin_a = 11
enc_left_pin_b = 10
sw_left_pin = 6
enc_right = gaugette.rotary_encoder.RotaryEncoder(enc_right_pin_a, enc_right_pin_b)
sw_right = gaugette.switch.Switch(sw_right_pin)
enc_left = gaugette.rotary_encoder.RotaryEncoder(enc_left_pin_a, enc_left_pin_b)
sw_left = gaugette.switch.Switch(sw_left_pin)

#Global Variables
timeNow_last = None
airplay_lock = False
mopidy_track_last = None
lcd_source_last = None
interface_state = 2		# 1=Radio 2=Spotify 3=Change Station/Playlist

def checkinput():
	enc_left_state_last = enc_left.rotation_state()
	right_count = 0
	left_count = 0
	
	while True:
		enc_right_delta = enc_right.get_delta()
		enc_left_state = enc_left.rotation_state()
		sw_right_state = sw_right.get_state()
		sw_left_state = sw_left.get_state()

		#RIGHT SWITCH
		if (sw_right_state == 1):
			if (right_count < 50):
				right_count += 1
			elif (right_count < 100): #Button held down
				right_count = 101 #So value is just registerd once
				print "right Hold"	
		else:
			if (right_count >0 and right_count < 50): #Button pressed
				print "right Press"

			right_count = 0 #Resetting Counter for next press.

		#RIGHT ENCODER
		if (enc_right_delta != 0):
			if (enc_right_delta<0):
				print ("Rotating to the right")
			elif (enc_right_delta>0):
				print ("Rotating to the left")

		#LEFT SWITCH
		if (sw_left_state == 1):
                        if (left_count < 50):
                                left_count += 1
                        elif (left_count < 100): #Button held down
                        	left_count = 101
                        	if (interface_state == 1):
					print "Byter till Spotify"
				elif (interface_state == 2):
					print "Byter till Radio"
                else:
                        if (left_count >0 and left_count < 50): #Button pressedv
                        	if (interface_state == 1):
					print "Like Current Song"
				elif (interface_state == 2):
					print "Byter Spellista"

                        left_count = 0 #Resetting Counter for next press.
		#LEFT ENCODER
		
		
		sleep(.01) #Sleeping for 0.01 sec so the CPU isnt loading at max.

#Staring Thread checkinput
thread.start_new_thread(checkinput, ())

while True:
	timeNow = datetime.now().strftime("%Y-%m-%d %H:%M")
	
	pArtist = subprocess.Popen("mpc current -f \"%artist% - %title%\"", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	mopidy_track, errSong = pArtist.communicate()
	pTrack = subprocess.Popen("mpc |grep \"#\"", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	track_info, errSong = pTrack.communicate()
	pairplay = subprocess.Popen("netstat -t |grep rfe", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	airplay, errAirplay = pairplay.communicate()

	track_info = track_info.split("#")
	track_info = track_info[1]
	track_info = track_info.split("   ")
	track_info = track_info[0]

	if (airplay and airplay_lock == False):
		lcd.setCursor(0,1)
		lcd.message("                    ")
		lcd.setCursor(0,2)
		lcd.message("                    ")
		lcd.setCursor(6,2)
		lcd.message("Airplay")
		airplay_lock = True
	elif (not airplay and airplay_lock == True):
		mopidy_track_last = None
		airplay_lock = False

	#LCD Update Time
	if (timeNow != timeNow_last):
		lcd.setCursor(0,0)
		lcd.message("[ "+timeNow+" ]")
		timeNow_last = timeNow
		print timeNow
		
	if (interface_state == 1):
		lcd_source = "Radio"
	elif (interface_state == 2):
		lcd_source = "Spotify       "+track_info
	if (lcd_source != lcd_source_last):
		lcd_source_last = lcd_source
		lcd.setCursor(0,1)
		lcd.message("                    ")
		lcd.setCursor(0,1)
		lcd.message(lcd_source)
	
	if (mopidy_track != mopidy_track_last):
		lcd.setCursor(0,2)
		lcd.message("                    ")
		lcd.setCursor(0,2)
		lcd.message(mopidy_track[:-1][:20])
		mopidy_track_last = mopidy_track
		print mopidy_track[:-1]
	
	sleep(0.01)
