import serial
import string
import subprocess
import time
from datetime import datetime

# 00 Telling arduino that Raspberry pi is up and running
# 01 Current station
# 02 Current Song playing
# 03 Current Time
# 04 Current Date

connected = False
internetConnected = False
toggle = 1

while 1:
	timeNow = datetime.now().strftime("%Y-%m-%d %H:%M")
	dateNow = datetime.now().strftime("%Y-%m-%d")
	
	if (internetConnected == True and connected == True):
		try:
			line = ser.readline()
			line = line.rstrip('\n')
			line = line.rstrip('\r')
		except:
			connected = False
		
		if (line == "save"):
			pMPC = subprocess.Popen("mpc current -f %title% >> saves.log", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		elif (line == "shutdown"):
			pMPC = subprocess.Popen("sudo shutdown -h 0", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		else:
			pMPC = subprocess.Popen("mpc "+line, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				
		pSong = subprocess.Popen("mpc current -f %title%", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		song, errSong = pSong.communicate()
		song = song[:-1]
		pStation = subprocess.Popen("mpc current -f %name%", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		station, errSong = pStation.communicate()
		station = station[:-1]
		
		pPlaying = subprocess.Popen("mpc |grep playing", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		playing, errSong = pPlaying.communicate()

		if (playing == ""):
			station = "NOT PLAYING"

		if (toggle == 1):
			ser.write("01"+station)
			print("01"+station)
			toggle = 2
		elif (toggle == 2):
			ser.write("02"+song)
			print("02"+song)
			toggle = 3
		elif (toggle == 3):
			ser.write("03"+timeNow)
			print("03"+timeNow)
			toggle = 1
	
	if not internetConnected:
		pOutput = subprocess.Popen("ping -c 1 8.8.8.8 |grep '1 received'", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		response, errOutput = pOutput.communicate()
		if (response != ""):
			internetConnected = True
		else:
			ser.write("01No Connection")
			print("01No Connection")
			time.sleep(1)
			ser.write("03"+timeNow)
			print("03"+timeNow)

	if not connected:
		try:
			ser = serial.Serial('/dev/ttyUSB0', 9600, timeout = 1)
			connected = True
			ser.write("00rpiup")
		except:
			print("No connection to serial")
			time.sleep(1)