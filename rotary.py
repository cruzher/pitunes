#!/usr/bin/python
import gaugette.rotary_encoder
import gaugette.switch
from time import sleep

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

def checkinput():
	global volume_current
	global mopidy_playing
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
		if (enc_left_delta != 0 and enc_left_seq == 2):
			if (enc_left_delta<0):
				subprocess.Popen("mpc next", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			elif (enc_left_delta>0):
				subprocess.Popen("mpc prev", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		
		sleep(.01) #Sleeping for 0.01 sec so the CPU isnt loading at max.
