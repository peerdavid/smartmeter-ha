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

# Setup podman
sudo apt-get -y install podman podman-compose

# sudo apt-get install python3-lxml -y

# Optionally install an mqtt broker
# sudo apt install mosquitto -y
# sudo systemctl enable mosquitto.service
