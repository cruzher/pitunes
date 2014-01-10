#!/bin/bash

#Making sure modules are loaded on boot
echo "i2c-bcm2708" | sudo tee -a /etc/modules
echo "i2c-dev" | sudo tee -a /etc/modules
echo "ipv6" | sudo tee -a /etc/modules

#Loading modlues manually
sudo modprobe i2c-bcm2708
sudo modprobe i2c-dev
sudo modprobe ipv6

cd $HOME

echo "(01/10) ADDING APT SOURCES/KEYS"
wget -q -O - http://apt.mopidy.com/mopidy.gpg | sudo apt-key add -
sudo wget -q -O /etc/apt/sources.list.d/mopidy.list http://apt.mopidy.com/mopidy.list

echo "(02/10) APT UPDATE / UPGRADE"
sudo aptitude update
sudo aptitude -y upgrade

echo "(03/10) INSTALLING DEPENDENCIES"
sudo aptitude install -y build-essential python-smbus i2c-tools python-dev python-rpi.gpio python-setuptools mpc supervisor

echo "(04/10) INSTALLING WIRINGPI2"
cd $HOME/pitunes/wiringPi/
./build
cd ..

echo "(05/10) INSTALLING WIRINGPI2-PYTHON"
git clone https://github.com/Gadgetoid/WiringPi2-Python.git
cd WiringPi2-Python/
sudo python setup.py install
cd ..

echo "(06/10) INSTALLING PY-GAUGETTE"
git clone git://github.com/guyc/py-gaugette.git
cd py-gaugette
git checkout wiringpi2
sudo python setup.py install
cd ..

echo "(07/10) INSTALLING MOPIDY"
sudo apt-get install -y mopidy mopidy-spotify
mkdir $HOME/.config/mopidy
cp $HOME/pitunes/conf/mopidy.conf $HOME/.config/mopidy/
sudo cp $HOME/pitunes/conf/supervisor/mopidy.conf /etc/supervisor/conf.d/
sudo supervisorctl update
sudo supervisorctl start mopidy

echo "(08/10) INSTALLING SHAIRPORT"
wget -q http://files.pixor.se/install.scripts/rpi/shairport.sh
chmod +x shairport.sh
./shairport.sh piTunes
rm shairport.sh

echo "(09/10) INSTALLING WEBSERVICE"
sudo apt-get install -y apache2 php5 mysql-server python-mysqldb
sudo apt-get install -y phpmyadmin #Not needed in final version

echo "(10/10) CONFIGURING APACHE2"
#Change User to pi
sudo sed -i "/export APACHE_RUN_USER=/ c\export APACHE_RUN_USER=pi" /etc/apache2/envvars
sudo sed -i "/export APACHE_RUN_GROUP=/ c\export APACHE_RUN_GROUP=pi" /etc/apache2/envvars

#Change DocumentRoot to webgui
sudo sed -i "/DocumentRoot / c\	DocumentRoot \/home\/pi\/pitunes\/webgui" /etc/apache2/sites-enabled/000-default

#remove lock folder
sudo rm -rf /var/lock/apache2/

#restart apache
sudo service apache2 restart

#Correcting right on config files
sudo chmod 777 /etc/init.d/shairport


#echo "(12/) START PITUNES.PY ON BOOT"
sudo cp $HOME/pitunes/conf/supervisor/pitunes.conf /etc/supervisor/conf.d/
sudo supervisorctl update
sudo supervisorctl start pitunes

echo ""
echo "FINISHED"