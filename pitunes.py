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
enc_vol_pin_a = 14
enc_vol_pin_b = 13
sw_vol_pin = 12
enc_stn_pin_a = 11
enc_stn_pin_b = 10
sw_stn_pin = 6
enc_volume = gaugette.rotary_encoder.RotaryEncoder(enc_vol_pin_a, enc_vol_pin_b)
sw_volume = gaugette.switch.Switch(sw_vol_pin)
enc_station = gaugette.rotary_encoder.RotaryEncoder(enc_stn_pin_a, enc_stn_pin_b)
sw_station = gaugette.switch.Switch(sw_stn_pin)

#Global Variables
timeNow_last = None
airplay_lock = False
mopidy_track_last = None
mopidy_artist_last = None

def checkinput():
	enc_vol_state_last = None
	enc_stn_state_last = None
	vol_count = 0
	stn_count = 0
	
	while True:
		enc_vol_state = enc_volume.rotation_state()
		enc_stn_state = enc_station.rotation_state()
		sw_vol_state = sw_volume.get_state()
		sw_stn_state = sw_station.get_state()

		#VOLUME SWITCH
		if (sw_vol_state == 1):
			if (vol_count < 50):
				vol_count += 1
			elif (vol_count < 100):
				print("vol hold")
				vol_count = 101
		else:
			if (vol_count >0 and vol_count < 50):
				print("vol push")

			#reset counter
			vol_count = 0

		#VOLUME ENCODER
		#if (enc_vol_state_last != enc_vol_state):
			#enc_vol_state_last = enc_vol_state
			#print ("rotating")


		#STATION SWITCH
		if (sw_stn_state == 1):
                        if (stn_count < 50):
                                stn_count += 1
                        elif (stn_count < 100):
                                print("stn hold")
                                stn_count = 101
                else:
                        if (stn_count >0 and stn_count < 50):
                                print("stn push")

                        #reset counter
                        stn_count = 0
		#STATION ENCODER
		sleep(.01)

#Staring Thread checkinput
thread.start_new_thread(checkinput, ())

while True:
	timeNow = datetime.now().strftime("%Y-%m-%d %H:%M")
	
	pSong = subprocess.Popen("mpc current -f %title%", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	mop_track, errSong = pSong.communicate()
	pArtist = subprocess.Popen("mpc current -f %artist%", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	mop_artist, errSong = pArtist.communicate()
	pairplay = subprocess.Popen("netstat -t |grep rfe", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	airplay, errAirplay = pairplay.communicate()

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
		mopidy_artist_last = None
		airplay_lock = False

	#LCD Update Time
	if (timeNow != timeNow_last):
		lcd.setCursor(0,0)
		lcd.message(timeNow)
		timeNow_last = timeNow
	
	if (mop_track != mopidy_track_last):
		lcd.setCursor(0,2)
		lcd.message("                    ")
		lcd.setCursor(0,2)
		lcd.message(mop_track[:20])
		mop_track_last = mop_track
		
	if (mop_artist != mopidy_artist_last):
		lcd.setCursor(0,1)
		lcd.message("                    ")
		lcd.setCursor(0,1)
		lcd.message(mop_artist[:20])
		mop_artist_last = mop_artist
	
	sleep(0.01)
