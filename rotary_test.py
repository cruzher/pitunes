import gaugette.rotary_encoder
import gaugette.switch
from time import sleep
import string
left_value = 0

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
enc_help_left = [0,0]


while True:
	enc_right_delta = enc_right.get_delta()
	enc_right_seq = enc_right.rotation_sequence()
	enc_left_delta = enc_left.get_delta()
	enc_left_seq = enc_left.rotation_sequence()
	sw_right_state = sw_right.get_state()
	sw_left_state = sw_left.get_state()

	if (enc_left_delta != 0):
		if (enc_left_seq == 2):
			print str(enc_left_seq) + ' ' + str(enc_help_left[0]) + str(enc_help_left[1])

		enc_help_left[1] = enc_help_left[0]
		enc_help_left[0] = enc_left_seq
	sleep(.01)