#! /usr/bin/env sh

set -o errexit
set -o nounset
set -o pipefail
if [[ "${TRACE-0}" == "1" ]]; then
    set -o xtrace
fi

# Install everything needed for the smart-meter connection and our app
sudo apt-get update
sudo apt-get upgrade -y

# Setup docker
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker $USER # requires logout and login to take effect

# sudo apt-get install python3-lxml -y

# Optionally install an mqtt broker
# sudo apt install mosquitto -y
# sudo systemctl enable mosquitto.service
