# Integration of Smartmeter (KaifaMA309) into HomeAssistant

This project integrates a Kaifa MA309 smartmeter (such as often in use by Tinetz) into HomeAssistant.
Thanks to [1] for this great work! This repository is basically a refactoring with some minor changes.

## Requirements

* Kaifa MA309 smart meter
* AES symmetrical key for decrypting MBus messages, this can be obtained by your grid provider
* Raspberry Pi 3/4
* USB to MBus *Slave* Adapter: <https://de.aliexpress.com/item/1005004874122617.html?gatewayAdapt=glo2deu>, around € 14,54
* RJ-12 cable

### Hardware Setup

Use the two inner wires and connect them to the USB to MBus adapter:

> Note: Not sure if polarity matters or not, so first measure the voltage with a meter; in my case the red wire has +27 V while the green wire was ground

![Wiring Schematics](docs/wiring-schematic.drawio.svg)

![Wiring](docs/wiring.jpg)

For more/alternative instructions, please follow [2].

### Software

```bash
./tools/setup.sh
pushd src
pip install -r requirements.txt
popd
```


To installl all requirements call `./setup.sh`. Next you either setup a broker
in HomeAssistant (install through addons) or you install your
own broker. If you want to setup a new broker, ensure that you enable external
acccess:

```bash
sudo nano /etc/mosquitto/mosquitto.conf

# Add the following lines at the end of the file:
listener 1883
allow_anonymous true

# Restart service
sudo systemctl restart mosquitto
```

Finally, add all the sensors to HomeAssistant. Open the `configuration.yaml` file
in HomeAssistant and add the following:

```yaml
sensor:
  - platform: mqtt
    name: "Energy In"
    unique_id: "smart_meter_energy_in"
    device_class: "energy"
    state_class: "total_increasing"
    unit_of_measurement: "kWh"
    state_topic: "home/smart_meter/energy_in"
  - platform: mqtt
    name: "Power In"
    unique_id: "smart_meter_power_in"
    device_class: "power"
    state_class: "measurement"
    unit_of_measurement: "kW"
    state_topic: "home/smart_meter/power_in"
  - platform: mqtt
    name: "Reactice Energy In"
    unique_id: "smart_meter_reactive_energy_in"
    device_class: "energy"
    state_class: "total_increasing"
    unit_of_measurement: "kWh"
    state_topic: "home/smart_meter/reactive_energy_in"
  - platform: mqtt
    name: "Energy Out"
    unique_id: "smart_meter_energy_out"
    device_class: "energy"
    state_class: "total_increasing"
    unit_of_measurement: "kWh"
    state_topic: "home/smart_meter/energy_out"
  - platform: mqtt
    name: "Power Out"
    unique_id: "smart_meter_power_out"
    device_class: "power"
    state_class: "measurement"
    unit_of_measurement: "kW"
    state_topic: "home/smart_meter/power_out"
  - platform: mqtt
    name: "Reactice Energy Out"
    unique_id: "smart_meter_reactive_energy_out"
    device_class: "energy"
    state_class: "total_increasing"
    unit_of_measurement: "kWh"
    state_topic: "home/smart_meter/reactive_energy_out"
  - platform: mqtt
    name: "Voltage L1"
    unique_id: "smart_meter_voltage_l1"
    device_class: "energy"
    state_class: "measurement"
    unit_of_measurement: "V"
    state_topic: "home/smart_meter/voltage_l1"
  - platform: mqtt
    name: "Voltage L2"
    unique_id: "smart_meter_voltage_l2"
    device_class: "energy"
    state_class: "measurement"
    unit_of_measurement: "V"
    state_topic: "home/smart_meter/voltage_l2"
  - platform: mqtt
    name: "Voltage L3"
    unique_id: "smart_meter_voltage_l3"
    device_class: "energy"
    state_class: "measurement"
    unit_of_measurement: "V"
    state_topic: "home/smart_meter/voltage_l3"
  - platform: mqtt
    name: "Current L1"
    unique_id: "smart_meter_current_l1"
    device_class: "energy"
    state_class: "measurement"
    unit_of_measurement: "A"
    state_topic: "home/smart_meter/current_l1"
  - platform: mqtt
    name: "Current L2"
    unique_id: "smart_meter_current_l2"
    device_class: "energy"
    state_class: "measurement"
    unit_of_measurement: "A"
    state_topic: "home/smart_meter/current_l2"
  - platform: mqtt
    name: "Current L3"
    unique_id: "smart_meter_current_l3"
    device_class: "energy"
    state_class: "measurement"
    unit_of_measurement: "A"
    state_topic: "home/smart_meter/current_l3"
```

Now restart your HA and you should see the sensors. To update
values you have to run the script.

# Run

You can simply run the script to test whether values are updated in HomeAssistant.

```bash
python ha_bridge.py --serial_key=YOUR_SMARMETER_KEY \
    --mqtt_server=YOUR_MQTT_SERVER \
    --mqtt_user=YOUR_USER \
    --mqtt_passwd=YOUR_PASSWORD
```

# Run as service

Create the following file with `sudo nano /etc/systemd/system/ha_bridge.service`:

```
[Unit]
Description=HomeAssistant Bridge
After=multi-user.target
[Service]
Type=simple
Restart=always
ExecStart=/usr/bin/python3 /home/pi/Dev/smartmeter-ha/ha_bridge.py --serial_key=YOUR_SMARMETER_KEY --mqtt_server=YOUR_MQTT_SERVER --mqtt_user=YOUR_USER --mqtt_passwd=YOUR_PASSWORD
[Install]
WantedBy=multi-user.target
```

Next reload the deamon and enable our service so it works also after a restart:
```
sudo systemctl daemon-reload
sudo systemctl enable ha_bridge.service
sudo systemctl start ha_bridge.service
```

To show output logs of your service, simply call

```
journalctl -f -u ha_bridge.service
```

# Thanks to

First of all thanks for "tirolerstefan" and Michael Reitbauer for the great work that
helped me to realize this project based on their implementations.

[1] <https://github.com/tirolerstefan/kaifa/>
[2] <https://www.michaelreitbauer.at/kaifa-ma309-auslesen-smart-meter-evn/>
[3] <https://www.tinetz.at/uploads/tx_bh/tinetz_smart-meter_beschreibung-kundenschnittstelle_001.pdf>