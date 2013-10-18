#!/bin/bash

echo "i2c-bcm2708" | sudo tee -a /etc/modules
echo "i2c-dev" | sudo tee -a /etc/modules
echo "ipv6" | sudo tee -a /etc/modules
sudo modprobe i2c-bcm2708
sudo modprobe i2c-dev
sudo modprobe ipv6

cd $HOME

echo "(01/10) ADDING APT SOURCES/KEYS"
wget -q -O - http://apt.mopidy.com/mopidy.gpg | sudo apt-key add -
sudo wget -q -O /etc/apt/sources.list.d/mopidy.list http://apt.mopidy.com/mopidy.list

echo "(02/10) APT UPDATE / UPGRADE"
sudo aptitude update > /dev/null
sudo aptitude -y upgrade > /dev/null

echo "(03/10) INSTALLING DEPENDENCIES"
sudo aptitude install -y build-essential python-smbus i2c-tools python-dev python-rpi.gpio python-setuptools mpc screen > /dev/null

echo "(04/10) INSTALLING WIRINGPI2"
cd $HOME/pitunes/wiringPi/
./build
cd ..

echo "(05/10) INSTALLING WIRINGPI2-PYTHON"
git clone https://github.com/Gadgetoid/WiringPi2-Python.git > /dev/null
cd WiringPi2-Python/
sudo python setup.py install > /dev/null
cd ..

echo "(06/10) INSTALLING PY-GAUGETTE"
git clone git://github.com/guyc/py-gaugette.git > /dev/null
cd py-gaugette
git checkout wiringpi2 > /dev/null
sudo python setup.py install > /dev/null
cd ..

echo "(07/10) INSTALLING MOPIDY"
sudo apt-get install -y mopidy > /dev/null
mkdir $HOME/.config/mopidy
cp $HOME/pitunes/conf/mopidy.conf $HOME/.config/mopidy/
sudo sed -i "/exit 0/ c\ " /etc/rc.local > /dev/null
echo "screen -dmS mopidy mopidy --config=/home/pi/.config/mopidy/mopidy.conf" | sudo tee -a /etc/rc.local > /dev/null
echo "exit 0" | sudo tee -a /etc/rc.local > /dev/null

echo "(08/10) INSTALLING SHAIRPORT"
wget -q http://files.pixor.se/install.scripts/rpi/shairport.sh
chmod +x shairport.sh
./shairport.sh piTunes > /dev/null
rm shairport.sh

echo "(09/10) INSTALLING WEBSERVICE"
sudo apt-get install -y lighttpd > /dev/null
sudo apt-get install -y mysql-server > /dev/null
sudo apt-get install -y php5-common php5-cgi php5 > /dev/null
sudo apt-get install -y php5-mysql > /dev/null
sudo apt-get install -y phpmyadmin > /dev/null
sudo lighty-enable-mod fastcgi-php > /dev/null
sudo service lighttpd force-reload > /dev/null

echo "(10/10) COPY WEBGUI TO APACHE-ROOT"
sudo chmod 777 /var/www
rm -rf /var/www/*
cp -R pitunes/webgui/* /var/www/

#echo "(12/) START PITUNES.PY ON BOOT"
#sudo sed -i "/exit 0/ c\ " /etc/rc.local
#echo "python /home/pi/pitunes/pitunes.py" | sudo tee -a /etc/rc.local
#echo "exit 0" | sudo tee -a /etc/rc.local

echo ""
echo "FINISHED"