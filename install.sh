#!/bin/bash

echo "#########################################"
echo "## Add these lines to /etc/modules     ##"
echo "## and reboot before you continue      ##"
echo "##                                     ##"
echo "## i2c-bcm2708                         ##"
echo "## i2c-dev                             ##"
echo "## ipv6                                ##"
echo "#########################################"

read -p "Have you done this? (y/n)" -n 1
echo ''
if [[ $REPLY =~ ^[Yy]$ ]]; then
	cd $HOME
	
	echo "###"
	echo "### APT UPDATE / UPGRADE"
	echo "###"
	sudo aptitude update > /dev/null
	sudo aptitude -y upgrade > /dev/null
	
	
	echo "###"
	echo "### INSTALLING DEPENDENCIES"
	echo "###"
	sudo aptitude install -y build-essential python-smbus i2c-tools python-dev python-rpi.gpio python-setuptools > /dev/null	
	
	
	echo "###"
	echo "### INSTALLING WIRINGPI2"
	echo "###"
	git clone git://git.drogon.net/wiringPi > /dev/null
	cd wiringPi
	./build > /dev/null
	cd ..
	#Wiringpi2-python
	git clone https://github.com/Gadgetoid/WiringPi2-Python.git > /dev/null
	cd WiringPi2-Python/
	sudo python setup.py install > /dev/null
	cd ..


	echo "###"
	echo "### INSTALLING PY-GAUGETTE"
	echo "###"
	git clone git://github.com/guyc/py-gaugette.git > /dev/null
	cd py-gaugette
	git checkout wiringpi2 > /dev/null
	sudo python setup.py install > /dev/null
	cd ..
	
	
	echo "###"
	echo "### INSTALLING ATXRASPI SHUTDOWNCHECK"
	echo "###"
	cp pitunes/shutdowncheck $HOME/
	sudo sed -i "/exit 0/ c\ " /etc/rc.local
	echo "(cd /home/pi && exec ./shutdowncheck) &" | sudo tee -a /etc/rc.local
	echo "exit 0" | sudo tee -a /etc/rc.local
	sudo bash ./shutdowncheck  > /dev/null &
	
	
	echo "###"
	echo "### INSTALLING MOPIDY"
	echo "###"
	wget -q -O - http://apt.mopidy.com/mopidy.gpg | sudo apt-key add -
	sudo wget -q -O /etc/apt/sources.list.d/mopidy.list http://apt.mopidy.com/mopidy.list
	sudo apt-get update > /dev/null
	sudo apt-get install -y mopidy > /dev/null
	mkdir $HOME/.config/mopidy
	cp $HOME/pitunes/conf/mopidy.conf $HOME/.config/mopidy/
	
	echo "###"
	echo "### INSTALLING SHAIRPORT"
	echo "###"
	wget http://files.pixor.se/install.scripts/rpi/shairport.sh
	chmod +x shairport.sh
	./shairport pitunes
	
	
	echo "###"
	echo "### INSTALLING TOOLS"
	echo "###"
	sudo aptitude install -y mpc screen > /dev/null
	
	
	echo "###"
	echo "### COPY WEBGUI TO APACHE-ROOT"
	echo "###"
	echo ""
	#sudo chmod 777 /var/www
	#rm -rf /var/www/*
	#cp -R pitunes/webgui/* /var/www/
	
	
	echo "###"
	echo "### START RASPBERRYPI.PY ON BOOT"
	echo "###"
	echo ""
	#sudo sed -i "/exit 0/ c\ " /etc/rc.local
	#echo "python /home/pi/pitunes/pitunes.py" | sudo tee -a /etc/rc.local
	#echo "exit 0" | sudo tee -a /etc/rc.local
fi