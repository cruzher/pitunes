#!/bin/bash

cd /home/pi/pitunes/
git pull
rm -rf /var/www/*
cp -R webgui/* /var/www/

