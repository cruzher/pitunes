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
	sudo aptitude update
	sudo aptitude -y upgrade
	
	
	echo "###"
	echo "### INSTALLING DEPENDENCIES"
	echo "###"
	sudo aptitude install -y build-essential python-smbus i2c-tools python-dev python-rpi.gpio python-setuptools		
	
	
	echo "###"
	echo "### INSTALLING WIRINGPI2"
	echo "###"
	git clone git://git.drogon.net/wiringPi
	cd wiringPi
	./build
	cd ..
	#Wiringpi2-python
	git clone https://github.com/Gadgetoid/WiringPi2-Python.git
	cd WiringPi2-Python/
	sudo python setup.py install
	cd ..


	echo "###"
	echo "### INSTALLING PY-GAUGETTE"
	echo "###"
	git clone git://github.com/guyc/py-gaugette.git
	cd py-gaugette
	git checkout wiringpi2
	sudo python setup.py install
	cd ..
	
	
	echo "###"
	echo "### INSTALLING ATXRASPI SHUTDOWNCHECK"
	echo "###"
	cp pitunes/shutdowncheck $HOME/
	sudo sed -i "/exit 0/ c\ " /etc/rc.local
	echo "(cd /home/pi && exec ./shutdowncheck) &" | sudo tee -a /etc/rc.local
	echo "exit 0" | sudo tee -a /etc/rc.local
	sudo bash ./shutdowncheck &
	
	
	echo "###"
	echo "### INSTALLING MOPIDY"
	echo "###"
	wget -q -O - http://apt.mopidy.com/mopidy.gpg | sudo apt-key add -
	sudo wget -q -O /etc/apt/sources.list.d/mopidy.list http://apt.mopidy.com/mopidy.list
	sudo apt-get update
	sudo apt-get install -y mopidy
	mkdir $HOME/.config/mopidy
	cp $HOME/pitunes/conf/mopidy.conf $HOME/.config/mopidy/
	
	
	echo "###"
	echo "### INSTALLING TOOLS"
	echo "###"
	#sudo aptitude install -y mpc php5 apache2 mysql-server
	
	
	echo "###"
	echo "### Setting audio to Analog out"
	echo "###"
	#sudo amixer cset numid=3 1 > /dev/null
	
	
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
	#sudo sed -i "/exit 0/ c\python /home/pi/pitunes/raspberrypi.py" /etc/rc.local
	#sudo echo "exit 0" >> /etc/rc.local
fi