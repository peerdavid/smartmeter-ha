#/usr/bin/python3

#
# Thanks to https://github.com/tirolerstefan/kaifa/blob/master/kaifareader.py
# for this really great work. This is basically a refactoring of this work
# to my needs...
#

import os
import sys
import serial
import argparse
import signal
import kaifa
import paho.mqtt.client as mqtt



#
# ARGS
#
parser = argparse.ArgumentParser(description='Integrate your smartmeter into HomeAssistant.')
parser.add_argument('--log_console', required=False, help='Log all energy values to console.')
parser.add_argument('--serial_port', default="/dev/ttyUSB0", help='Port of M-BUS to USB adapter.')
parser.add_argument('--serial_key', required=False, default=os.environ.get('SERIAL_KEY'), help='Your private smartmeter key. See also https://www.netz-noe.at/Download-(1)/Smart-Meter/218_9_SmartMeter_Kundenschnittstelle_lektoriert_14.aspx')
parser.add_argument('--mqtt_server', default=os.environ.get('MQTT_SERVER'), help='MQTT server host.')
parser.add_argument('--mqtt_port', default=1883, help='MQTT server port.')
parser.add_argument('--mqtt_user', default=os.environ.get('MQTT_USER'), help='MQTT user.')
parser.add_argument('--mqtt_passwd', default=os.environ.get('MQTT_PASSWD'), help='MQTT password.')
args = parser.parse_args()


#
# HELPER
#
def create_mqtt_client():
    mqtt_client = mqtt.Client("kaifareader")
    mqtt_client.username_pw_set(args.mqtt_user, args.mqtt_passwd)
    mqtt_client.connect(args.mqtt_server, port=args.mqtt_port)
    mqtt_client.loop_start()
    return mqtt_client


def create_serial_client():
    return serial.Serial(
        port = args.serial_port,
        baudrate = 2400,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
    )


#
# M A I N
#
def main():

    # Create clients
    serial_conn = create_serial_client()
    mqtt_client = create_mqtt_client()

    # Ensure that we correctly disconnect from serial
    def signal_handler(sig, frame):
        serial_conn.close()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    # Update MQTT broker forever
    while True:
        try:
            energy_object = kaifa.read_energy_data(serial_conn, args.serial_key)
            for entry in energy_object.data:
                mqtt_client.publish(f"home/smart_meter/{entry}", energy_object.data[entry])

            if args.log_console:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(energy_object)
            else:
                print("Successfully updated HomeAssistant sensors.")
        except Exception as e:
            print(f"(Error) Update failed with {e}")


if __name__ == "__main__":
    main()
