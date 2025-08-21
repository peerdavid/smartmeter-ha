# Quadlet Deployment Guide

This directory contains Quadlet configuration files for running the `mbus_to_usb` service with Podman and systemd.

## Files

- `mbus_to_usb.container` - Quadlet container configuration
- `mbus_to_usb.env.example` - Environment variables template
- `build-container.sh` - Script to build the container image

## Prerequisites

- Podman 4.4+ with Quadlet support
- systemd
- Access to USB device (typically `/dev/ttyUSB0`)

## Setup Instructions

### 1. Build the Container Image

First, build the container image:

```bash
./build-container.sh
```

### 2. Configure Environment

Copy the environment template and configure your settings:

```bash
cp mbus_to_usb.env.example mbus_to_usb.env
```

Edit `mbus_to_usb.env` with your specific values:

- `SERIAL_KEY`: Your smart meter serial key
- `MQTT_SERVER`: Your MQTT broker hostname/IP
- `MQTT_PORT`: MQTT broker port (usually 1883)
- `MQTT_USER`: MQTT username
- `MQTT_PASSWD`: MQTT password
- `HOST_USB_DEVICE`: USB device path (usually `/dev/ttyUSB0`)

### 3. Install Quadlet Files

For system-wide service (requires root):

```bash
sudo mkdir -p /etc/containers/systemd
cd tools/systemd
sudo cp mbus_to_usb.container /etc/containers/systemd/
sudo cp cp ../../.env /etc/containers/systemd/mbus_to_usb.env
sudo systemctl daemon-reload
sudo systemctl enable --now mbus_to_usb.service
```


## Managing the Service

### Check Service Status

```bash
systemctl --user status mbus_to_usb.service
```

### View Logs

```bash
journalctl --user -u mbus_to_usb.service -f
```

### Stop Service

```bash
systemctl --user stop mbus_to_usb.service
```

### Restart Service

```bash
systemctl --user restart mbus_to_usb.service
```

## USB Device Permissions

If you encounter permission issues with the USB device, you may need to:

1. Add your user to the `dialout` group:

   ```bash
   sudo usermod -a -G dialout $USER
   ```

2. Create a udev rule for the device (create `/etc/udev/rules.d/99-mbus-usb.rules`):

   ```text
   SUBSYSTEM=="tty", ATTRS{idVendor}=="your_vendor_id", ATTRS{idProduct}=="your_product_id", GROUP="dialout", MODE="0664"
   ```

3. Reload udev rules:

   ```bash
   sudo udevadm control --reload-rules && sudo udevadm trigger
   ```

## Differences from Docker Compose

- Environment variables are loaded from a file instead of being defined inline
- Service runs as a systemd service with better integration
- Automatic restart and dependency management through systemd
- Container logs are available through journalctl
- No need for a separate Docker Compose daemon

## Troubleshooting

1. **Service fails to start**: Check logs with `journalctl --user -u mbus_to_usb.service`
2. **USB device not accessible**: Verify device path and permissions
3. **Environment variables not loaded**: Ensure `.env` file is in the same directory as `.container` file
4. **Container image not found**: Run `./build-container.sh` to build the image
