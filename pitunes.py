#!/usr/bin/python

import string
import subprocess
import thread
from rotary import checkinput
from time import sleep
from datetime import datetime
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import gaugette.rotary_encoder
import gaugette.switch

#LCD
lcd = Adafruit_CharLCDPlate()
lcd.begin(20, 4)
lcd.clear()

#Global Variables
lcd_timeNow = None
lcd_song = None
lcd_source_last = None
volume_current = 10
airplay_lock = False
interface_state = 2		# 1=Radio 2=Spotify 3=Change Station/Playlist
mopidy_playing = False

def changevolume():
	global volume_current
	volume_last = 0
	
	while True:
		if (volume_last != volume_current):
			print volume_current
			volume_last = volume_current
		sleep(.01)

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
		lcd.setCursor(0,1)
		lcd.message("                    ")
		lcd.setCursor(0,2)
		lcd.message("                    ")
		lcd.setCursor(6,2)
		lcd.message("Airplay")
		airplay_lock = True
	elif (not airplay and airplay_lock == True):
		lcd_song = None
		airplay_lock = False

	#LCD Update Time
	if (timeNow != lcd_timeNow):
		lcd.setCursor(0,0)
		lcd.message(timeNow)
		lcd_timeNow = timeNow
		print "time: "+timeNow
		
	if (interface_state == 1):
		lcd_source = "Radio"
	elif (interface_state == 2):
		lcd_source = "Spotify     "
	if (lcd_source_last != lcd_source):
		lcd_source_last = lcd_source
		lcd.setCursor(0,1)
		lcd.message("                    ")
		lcd.setCursor(0,1)
		lcd.message(lcd_source)
		print "Source: "+lcd_source
	
	if (mopidy_track != lcd_song):
		lcd.setCursor(0,2)
		lcd.message("                    ")
		lcd.setCursor(0,2)
		lcd.message(mopidy_track[:-1][:20])
		lcd_song = mopidy_track
		print "Song: "+mopidy_track[:-1]
	
	sleep(0.01)
