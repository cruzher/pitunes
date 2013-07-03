import string
import subprocess
import time
from datetime import datetime
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import gaugette.rotary_encoder
import gaugette.switch

#LCD
lcd = Adafruit_CharLCDPlate()
lcd.begin(20, 4)

lcd.clear()
lcd.setCursor(0,0)
lcd.message("Mekk");

#Rotary Encoders
volume_a = 14
volume_b = 13
volume_sw = 12

volume_enc = gaugette.rotary_encoder.RotaryEncoder(volume_a, volume_b)
volume_switch = gaugette.switch.Switch(volume_sw)

vol_sw_last = None
vol_state_last = None

station_a = 11
station_b = 10
station_sw = 6

station_enc = gaugette.rotary_encoder.RotaryEncoder(station_a, station_b)
station_switch = gaugette.switch.Switch(station_sw)

stn_sw_last = None
stn_state_last = None


while True:
	vol_state = volume_enc.rotation_state()
	vol_sw = volume_switch.get_state()
	stn_state = station_enc.rotation_state()
	stn_sw = station_switch.get_state()
	
	if (vol_state != vol_state_last or vol_sw != vol_sw_last):
		vol_state_last = vol_state
		vol_sw_last = vol_sw
		
		if (vol_sw==1):
			mekk = subprocess.Popen("mpc play", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			
	if (stn_state != stn_state_last or stn_sw != stn_sw_last):
		stn_state_last = stn_state
		stn_sw_last = stn_sw
		
		if (stn_sw==1):
			mekk = subprocess.Popen("mpc stop", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
	sleep(0.01)
