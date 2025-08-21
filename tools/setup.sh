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

sudo apt-get -y install podman podman-compose

# allow local quadlets to run on startup
loginctl enable-linger

ln -s systemd/mbus_to_usb.container ~/.config/containers/systemd/mbus_to_usb.container
