#!/bin/bash

# Install everything needed for the smart-meter connection and our app
sudo apt-get udpate
sudo apt-get install python3-lxml python-lxml -y
pip3 install -r requirements.txt

# Optionally install an mqtt broker
# sudo apt install mosquitto -y
# sudo systemctl enable mosquitto.service
