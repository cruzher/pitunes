#!/usr/bin/python

import string
from subprocess import Popen, PIPE

current_song = Popen("mpc |head -2 |tail -1", shell=True, stdout=PIPE).stdout.read()
current_song = current_song.split(" ")
print current_song