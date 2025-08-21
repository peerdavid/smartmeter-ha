#!/bin/bash

# Build script for mbus_to_usb container image
# This script builds the container image that can be used with the Quadlet service

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
IMAGE_NAME="localhost/mbus_to_usb:latest"

echo "Building mbus_to_usb container image..."

# Build the container image using podman
podman build \
    --file "${SCRIPT_DIR}/Containerfile" \
    --tag "${IMAGE_NAME}" \
    "${SCRIPT_DIR}"

echo "Container image built successfully: ${IMAGE_NAME}"
echo ""
echo "To use with Quadlet:"
echo "1. Copy mbus_to_usb.env.example to mbus_to_usb.env and adjust the values"
echo "2. Copy mbus_to_usb.container to ~/.config/containers/systemd/ (or /etc/containers/systemd/ for system-wide)"
echo "3. Run: systemctl --user daemon-reload"
echo "4. Run: systemctl --user start mbus_to_usb.service"
echo "5. Run: systemctl --user enable mbus_to_usb.service (to start automatically on boot)"
