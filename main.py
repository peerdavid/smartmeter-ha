#/usr/bin/python3
import os
import sys
import serial
import argparse
import signal
import kaifa


#
# ARGS
#
parser = argparse.ArgumentParser(description='Integrate your smartmeter into HomeAssistant.')
parser.add_argument('--port', default="/dev/ttyUSB0", help='Port of M-BUS to USB adapter.')
parser.add_argument('--key', required=True, help='Your private smartmeter key. See also https://www.netz-noe.at/Download-(1)/Smart-Meter/218_9_SmartMeter_Kundenschnittstelle_lektoriert_14.aspx')
args = parser.parse_args()



#
# M A I N
#
def main():
    serial_conn = serial.Serial(
        port = args.port,
        baudrate = 2400,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
    )

    # Ensure that we disconnect from serial
    def signal_handler(sig, frame):
        serial_conn.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)


    while True:
        data = kaifa.read_energy_data(serial_conn, args.key)
        os.system('cls' if os.name == 'nt' else 'clear')
        print(data)


if __name__ == "__main__":
    main()
