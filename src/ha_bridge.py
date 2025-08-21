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
import json
import logging
import sentry_sdk

#
# ARGS
#
parser = argparse.ArgumentParser(description='Integrate your smartmeter into HomeAssistant.')
parser.add_argument('--log_console', required=False, help='Log all energy values to console.')
parser.add_argument('--serial_port', default="/dev/ttyUSB0", help='Port of M-BUS to USB adapter.')
parser.add_argument('--serial_key', required=False, default=os.environ.get('SERIAL_KEY'), help='Your private smartmeter key. See also https://www.netz-noe.at/Download-(1)/Smart-Meter/218_9_SmartMeter_Kundenschnittstelle_lektoriert_14.aspx')
parser.add_argument('--mqtt_server', default=os.environ.get('MQTT_SERVER'), help='MQTT server host.')
parser.add_argument('--mqtt_port', type=int, default=os.environ.get('MQTT_PORT'), help='MQTT server port.')
parser.add_argument('--mqtt_user', default=os.environ.get('MQTT_USER'), help='MQTT user.')
parser.add_argument('--mqtt_passwd', default=os.environ.get('MQTT_PASSWD'), help='MQTT password.')
parser.add_argument('--sentry_url', default=os.environ.get('SENTRY_URL'), help='Sentry error url, e.g., `https://749459935037466094fd53656df$6f629@o131075.ingest.sentry.io/2505107393847584`')
args = parser.parse_args()


#
# HELPER
#
def create_mqtt_client():
    mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "kaifareader")
    mqttc.username_pw_set(args.mqtt_user, args.mqtt_passwd)
    mqttc.connect(args.mqtt_server, port=args.mqtt_port)
    mqttc.loop_start()
    return mqttc


def create_serial_client():
    return serial.Serial(
        port = args.serial_port,
        baudrate = 2400,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
    )

def initialize_sentry():
    if(not args.sentry_url):
        sentry_sdk.init(
            dsn=args.sentry_url,

            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            # We recommend adjusting this value in production.
            traces_sample_rate=0.0
        )

#
# M A I N
#
def main():
    # Create clients
    serial_conn = create_serial_client()
    mqttc = create_mqtt_client()
    initialize_sentry()

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
                mqttc.publish(f"home/smart_meter/{entry}", energy_object.data[entry])

            energy_object_str = json.dumps(energy_object.data)
            mqttc.publish(f"home/smart_meter/json", energy_object_str)

            if args.log_console:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(energy_object)
            else:
                print("Successfully updated HomeAssistant sensors.")
        except Exception as e:
            logging.exception("Unhandled Exception, quitting")
            sys.exit(-1)

if __name__ == "__main__":
    main()
