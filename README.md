# Integration of Smartmeter(KaifaMA309) into HomeAssistant
This project integrates a KaifaMA309 (TINETZ) smartmeter into HomeAssistant.
Thanks to [1] for this great work! This repository is basically
a refactoring with some minor changes.


# Hardware
Please follow [2] to setup your hardware. I use exactly this hardware setup and it works fine.

# Setup Raspberry
I first had the problem that `/dev/ttyUSB0` was not shown after installing a
new Raspberry Pi 4 and connecting the USB to MBUS converter. It seems that
there is a kernel bug and a kernel downgrade, therefore, solves this issue.
I made the downgrade through `sudo rpi-update da70b00`.

To installl all requirements call `./setup.sh`. Next you either setup a broker
in HomeAssistant (install through addons) or you install your
own broker. If you want to setup a new broker, ensure that you enable external
acccess:

```
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
You can simiply run the script to test whether values are updated in HomeAssistant.
```bash
python ha_bridge.py --serial_key=YOUR_SMARMETER_KEY \
    --mqtt_server=YOUR_MQTT_SERVER \
    --mqtt_user=YOUR_USER \
    --mqtt_passwd=YOUR_PASSWORD
```


# Thanks to
First of all thanks for "tirolerstefan" and Michael Reitbauer for the great work that
helped me to realize this project based on their implementations.
<br /><br />
[1] https://github.com/tirolerstefan/kaifa/ <br />
[2] https://www.michaelreitbauer.at/kaifa-ma309-auslesen-smart-meter-evn/ <br />
[3] https://www.tinetz.at/uploads/tx_bh/tinetz_smart-meter_beschreibung-kundenschnittstelle_001.pdf <br />