#!/bin/bash

# Install everything needed for the smart-meter connection and our app
sudo apt-get udpate
sudo apt-get upgrade -y

# Setup docker
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# sudo apt-get install python3-lxml -y

# Optionally install an mqtt broker
# sudo apt install mosquitto -y
# sudo systemctl enable mosquitto.service
