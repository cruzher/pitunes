#!/bin/bash
#Airplay monitor script v1.0 for use with MPD and shairport by James Hildebrandt 2013
#Requires MPC be installed for command line control of MPD
#Script checks to see if shairport has an active stream, if so it pauses MPD via MPC
#Once Airplay stream ends it resumes MPD
COUNTER=1
AIRPLAY_STATE=0
CURR_STATE=0
PREV_STATE=0
MPC_STATE=0
#AIRPLAY_ON=""
while [ $COUNTER == 1 ]; do
        sleep 5
        AIRPLAY_STATE=`netstat -t | grep rfe` #Check if anyone is playing music using airplay and set the output as variable
        MPC_STATE=`mpc | head -2 | tail -1 | awk '{print $1}'` #Check the state of mpc to see if it is playing and set the output as variable
        if [[ $AIRPLAY_STATE ]]; then #If AIRPLAY_STATE is not empty then someone is connected so ...
                echo on > /dev/shm/airplay_state #Write "on" to file airplay_state in ram
                CURR_STATE=1
                PREV_STATE=1
        else
                echo off > /dev/shm/airplay_state #Otherwise write "off" to file airplay_state in ram
                CURR_STATE=0
        fi
        if [[ $AIRPLAY_STATE ]] && [ $MPC_STATE == "[playing]" ]; then #if someone is connected via airplay and mpc is playing
                mpc pause -q  #Then pause mpc and do it quietly so there is no output returned
        fi
        if [ $CURR_STATE == "0" ] && [ $MPC_STATE == "[paused]" ] && [ $PREV_STATE == "1" ]; then #If current airplay state is off, mpc is paused, and prev state is 1 then resume playing mpc
                mpc play -q
                PREV_STATE=0
        fi
done
