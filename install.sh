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
	
	echo "(01/) ADDING APT SOURCES/KEYS"
	wget -q -O - http://apt.mopidy.com/mopidy.gpg | sudo apt-key add -
	sudo wget -q -O /etc/apt/sources.list.d/mopidy.list http://apt.mopidy.com/mopidy.list
	
	echo "(02/) APT UPDATE / UPGRADE"
	sudo aptitude update > /dev/null
	sudo aptitude -y upgrade > /dev/null
	
	
	echo "(03/) INSTALLING DEPENDENCIES"
	sudo aptitude install -y build-essential python-smbus i2c-tools python-dev python-rpi.gpio python-setuptools mpc screen > /dev/null	
	
	
	
	echo "(04/) INSTALLING WIRINGPI2"
	git clone git://git.drogon.net/wiringPi > /dev/null
	cd wiringPi
	./build > /dev/null
	cd ..
	
	echo "(05/) INSTALLING WIRINGPI2-PYTHON"
	git clone https://github.com/Gadgetoid/WiringPi2-Python.git > /dev/null
	cd WiringPi2-Python/
	sudo python setup.py install > /dev/null
	cd ..
	
	echo "(06/) INSTALLING PY-GAUGETTE"
	git clone git://github.com/guyc/py-gaugette.git > /dev/null
	cd py-gaugette
	git checkout wiringpi2 > /dev/null
	sudo python setup.py install > /dev/null
	cd ..
	
	echo "(07/) INSTALLING ATXRASPI SHUTDOWNCHECK"
	cp pitunes/shutdowncheck $HOME/
	sudo sed -i "/exit 0/ c\ " /etc/rc.local
	echo "(cd /home/pi && exec ./shutdowncheck) &" | sudo tee -a /etc/rc.local
	echo "exit 0" | sudo tee -a /etc/rc.local
	sudo bash ./shutdowncheck  > /dev/null &
	
	echo "(08/) INSTALLING MOPIDY"
	sudo apt-get install -y mopidy > /dev/null
	mkdir $HOME/.config/mopidy
	cp $HOME/pitunes/conf/mopidy.conf $HOME/.config/mopidy/
	
	echo "(09/) INSTALLING SHAIRPORT"
	wget -q http://files.pixor.se/install.scripts/rpi/shairport.sh
	chmod +x shairport.sh
	./shairport.sh piTunes
	rm shairport.sh
	
	#echo "(10/) INSTALLING APACHE"
	#sudo aptitude install -y apache2 > /dev/null
	
	#echo "(11/) COPY WEBGUI TO APACHE-ROOT"
	#sudo chmod 777 /var/www
	#rm -rf /var/www/*
	#cp -R pitunes/webgui/* /var/www/
	
	#echo "(12/) START PITUNES.PY ON BOOT"
	#sudo sed -i "/exit 0/ c\ " /etc/rc.local
	#echo "python /home/pi/pitunes/pitunes.py" | sudo tee -a /etc/rc.local
	#echo "exit 0" | sudo tee -a /etc/rc.local
	
	echo ""
	echo "FINISHED"

else
	echo "Please run this script again reboot"
	read -p "Continue and add lines? (this will reboot)" -n 1
	echo ''
	if [[ $REPLY =~ ^[Yy]$ ]]; then	
		echo "i2c-bcm2708" | sudo tee -a /etc/modules
		echo "i2c-dev" | sudo tee -a /etc/modules
		echo "ipv6" | sudo tee -a /etc/modules
		sudo reboot
	fi
fi